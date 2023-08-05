"""Scalene: a high-performance, high-precision CPU *and* memory profiler for Python.

    Scalene uses interrupt-driven sampling for CPU profiling. For memory
    profiling, it uses a similar mechanism but with interrupts generated
    by a "sampling memory allocator" that produces signals everytime the
    heap grows or shrinks by a certain amount. See libscalene.cpp for
    details (sampling logic is in include/sampleheap.hpp).

    by Emery Berger
    https://emeryberger.com

    usage: # for CPU profiling only
            python -m Scalene test/testme.py
            # for CPU and memory profiling (Mac OS X)
            DYLD_INSERT_LIBRARIES=$PWD/libscalene.dylib PYTHONMALLOC=malloc python -m scalene test/testme.py
            # for CPU and memory profiling (Linux)
            LD_PRELOAD=$PWD/libscalene.so PYTHONMALLOC=malloc python -m scalene test/testme.py

"""

# import random
import sys
import atexit
import signal
import math
from collections import defaultdict
import time
from pathlib import Path
import os
import traceback
import argparse
from contextlib import contextmanager
from functools import lru_cache
from textwrap import dedent

# Logic to ignore @profile decorators.
import builtins
try:
    builtins.profile
except AttributeError:
    # No line profiler, provide a pass-through version
    def profile(func): return func
    builtins.profile = profile


the_globals = {
    '__name__': '__main__',
    '__doc__': None,
    '__package__': None,
    '__loader__': globals()['__loader__'],
    '__spec__': None,
    '__annotations__': {},
    '__builtins__': globals()['__builtins__'],
    '__file__': None,
    '__cached__': None,
}

assert sys.version_info[0] == 3 and sys.version_info[1] >= 5, "Scalene requires Python version 3.5 or above."

# Scalene currently only supports Unix-like operating systems; in particular, Linux and Mac OS X.
if sys.platform == 'win32':
    print("Scalene currently does not support Windows, but works on Linux and Mac OS X.")
    sys.exit(-1)

class Scalene():
    """The Scalene profiler itself."""
    # Statistics counters.
    cpu_samples_python            = defaultdict(lambda: defaultdict(float))  # CPU    samples for each location in the program
                                                                           #        spent in the interpreter
    cpu_samples_c                 = defaultdict(lambda: defaultdict(float))  # CPU    samples for each location in the program
                                                                           #        spent in C / libraries / system calls
    memory_malloc_samples         = defaultdict(lambda: defaultdict(float))  # free samples for each location in the program
    memory_malloc_count           = defaultdict(lambda: defaultdict(int))  # number of times samples were added for the above
    memory_free_samples           = defaultdict(lambda: defaultdict(float))  # malloc samples for each location in the program
    memory_free_count             = defaultdict(lambda: defaultdict(int))  # number of times samples were added for the above
    memory_max_samples            = defaultdict(lambda: defaultdict(float))  # malloc samples for each location in the program
    total_max_samples             = 0
    total_cpu_samples             = 0.0            # how many CPU    samples have been collected.
    total_memory_free_samples     = 0              # "   "    malloc "       "    "    "
    total_memory_malloc_samples   = 0              # "   "    free   "       "    "    "
    current_footprint             = 0
    max_footprint                 = 0
    mean_signal_interval          = 0.01           # mean seconds between interrupts for CPU sampling.
    last_signal_interval          = 0.01           # last num seconds between interrupts for CPU sampling.
    original_path                 = ""             # original working directory.
    program_path                  = ""             # path for the program being profiled.
    output_file                   = ""             # where we write profile info.
    output_profile_interval       = float("inf")   # how long between outputting stats during execution.
    next_output_time              = float("inf")   # when do we output the next profile.
    elapsed_time                  = 0              # total time spent in program being profiled.

    # Things that need to be in sync with include/sampleheap.hpp:
    
    malloc_signal_filename        = "/tmp/scalene-malloc-signal"             # file to communicate the number of malloc samples
    free_signal_filename          = "/tmp/scalene-free-signal"               # "    "  "           "   "      "  free   "
    #malloc_sampling_rate          = 16777259 # 1048583  # we get signals after this many bytes are allocated.
    #free_sampling_rate            = 16777289 # 1048589  # as above, for frees.

    # NB: the below MUST BE IN SYNC WITH include/sampleheap.hpp!
    malloc_sampling_rate          = 1048583 # 33554467 # 16777259 # 1048583  # we get signals after this many bytes are allocated.
    free_sampling_rate            = 1048589 # 33554473 # 16777289 # 1048589  # as above, for frees.
    
    # The specific signals we use. Malloc and free signals are generated by include/sampleheap.hpp.

    cpu_signal    = signal.SIGVTALRM
    malloc_signal = signal.SIGXCPU
    free_signal   = signal.SIGPROF

    # Program-specific information.
    program_being_profiled = ""          # the name of the program being profiled.
    program_path           = ""          # the path "  "   "       "     "


    @staticmethod
    def set_timer_signal(use_wallclock_time = False):
        if use_wallclock_time:
            Scalene.cpu_timer_signal = signal.ITIMER_REAL
        else:
            Scalene.cpu_timer_signal = signal.ITIMER_VIRTUAL
            
        # Now set the appropriate timer signal.
        if Scalene.cpu_timer_signal == signal.ITIMER_REAL:
            Scalene.cpu_signal  = signal.SIGALRM
        elif Scalene.cpu_timer_signal == signal.ITIMER_VIRTUAL:
            Scalene.cpu_signal = signal.SIGVTALRM
        elif Scalene.cpu_timer_signal == signal.ITIMER_PROF:
            # NOT SUPPORTED
            assert False, "ITIMER_PROF is not currently supported."

    @staticmethod
    def enable_signals():
        # Set up the signal handler to handle periodic timer interrupts (for CPU).
        signal.signal(Scalene.cpu_signal, Scalene.cpu_signal_handler)
        # Set up the signal handler to handle malloc/free interrupts (for memory allocations).
        signal.signal(Scalene.malloc_signal, Scalene.alloc_event_signal_handler)
        signal.signal(Scalene.free_signal, Scalene.alloc_event_signal_handler)
        #        signal.signal(Scalene.malloc_signal, Scalene.malloc_signal_handler)
        #        signal.signal(Scalene.free_signal, Scalene.free_signal_handler)
        # Turn on the CPU profiling timer to run every signal_interval seconds.
        signal.setitimer(Scalene.cpu_timer_signal, Scalene.mean_signal_interval, Scalene.mean_signal_interval)
        Scalene.last_signal_time = Scalene.gettime()
        
    
    @staticmethod
    def gettime():
        """High-precision timer of time spent running in or on behalf of this process."""
        return time.process_time()

    def __init__(self, program_being_profiled):
        # Register the exit handler to run when the program terminates or we quit.
        atexit.register(Scalene.exit_handler)
        # Store relevant names (program, path).
        Scalene.program_being_profiled = os.path.abspath(program_being_profiled)
        Scalene.program_path = os.path.dirname(Scalene.program_being_profiled)
        # Set signal handlers.


    @staticmethod
    def cpu_signal_handler(_, frame):
        """Handle interrupts for CPU profiling."""
        # Record how long it has been since we received a timer
        # before.  See the logic below.
        now = Scalene.gettime()
        # If it's time to print some profiling info, do so.
        if now >= Scalene.next_output_time:
            # Print out the profile.
            # Set the next output time, stop signals, print the profile, and then start signals again.
            Scalene.next_output_time += Scalene.output_profile_interval
            Scalene.stop()
            Scalene.output_profiles()
            Scalene.start()
        fname = frame.f_code.co_filename
        # Record samples only for files we care about.
        if (len(fname)) == 0:
            # 'eval/compile' gives no f_code.co_filename.
            # We have to look back into the outer frame in order to check the co_filename.
            fname = frame.f_back.f_code.co_filename
        if not Scalene.should_trace(fname):
            Scalene.last_signal_time = Scalene.gettime()
            # Currently disabled: random sampling for CPU timing. Just use the same interval all the time.
            # Scalene.last_signal_interval = random.uniform(Scalene.mean_signal_interval / 2, Scalene.mean_signal_interval * 3 / 2)
            # signal.setitimer(Scalene.cpu_timer_signal, Scalene.last_signal_interval, Scalene.last_signal_interval)
            return
        # Here we take advantage of an apparent limitation of Python:
        # it only delivers signals after the interpreter has given up
        # control. This seems to mean that sampling is limited to code
        # running purely in the interpreter, and in fact, that was a limitation
        # of the first version of Scalene.
        #
        # (cf. https://docs.python.org/3.9/library/signal.html#execution-of-python-signal-handlers)
        #
        # However: lemons -> lemonade: this "problem" is in fact
        # an effective way to separate out time spent in
        # Python vs. time spent in native code "for free"!  If we get
        # the signal immediately, we must be running in the
        # interpreter. On the other hand, if it was delayed, that means
        # we are running code OUTSIDE the interpreter, e.g.,
        # native code (be it inside of Python or in a library). We
        # account for this time by tracking the elapsed (process) time
        # and compare it to the interval, and add any computed delay
        # (as if it were sampled) to the C counter.
        python_time = Scalene.last_signal_interval
        c_time = now - Scalene.last_signal_time - Scalene.last_signal_interval
        Scalene.cpu_samples_python[fname][frame.f_lineno] += python_time
        Scalene.cpu_samples_c[fname][frame.f_lineno] += c_time
        Scalene.total_cpu_samples += python_time + c_time
        # disabled randomness for now
        # Scalene.last_signal_interval = random.uniform(Scalene.mean_signal_interval / 2, Scalene.mean_signal_interval * 3 / 2)
        # signal.setitimer(Scalene.cpu_timer_signal, Scalene.last_signal_interval, Scalene.last_signal_interval)
        Scalene.last_signal_time = Scalene.gettime()
        return

    @staticmethod
    def malloc_signal_handler(_, frame):
        """Handle interrupts for memory profiling (mallocs)."""
        fname = frame.f_code.co_filename
        # Record samples only for files we care about.
        if not Scalene.should_trace(fname):
            return
        count = 1.0
        lineno = frame.f_lineno
        read_something = False
        try:
            with open(Scalene.malloc_signal_filename, "r") as f:
                for l, count_str in enumerate(f, 1):
                    read_something = True
                    count_str = count_str.rstrip()
                    count = float(count_str)
                    Scalene.memory_malloc_samples[fname][lineno] += count
                    # print(str(lineno) + " - SCALENE (" + str(l) + ") : malloc = " + str(count) + ", " + str(Scalene.memory_malloc_samples[fname][lineno]))
                    Scalene.total_memory_malloc_samples += count
                    Scalene.current_footprint += count
            if Scalene.current_footprint > Scalene.max_footprint:
                #            Scalene.memory_max_samples[fname][lineno] += count
                #            Scalene.total_max_samples += count
                Scalene.max_footprint = Scalene.current_footprint
            os.remove(Scalene.malloc_signal_filename)
        except Exception as e:
            # print(e)
            pass
        if read_something:
            Scalene.memory_malloc_count[fname][lineno] += 1
        return

    @staticmethod
    def free_signal_handler(_, frame):
        """Handle interrupts for memory profiling (frees)."""
        fname = frame.f_code.co_filename
        # Record samples only for files we care about.
        if not Scalene.should_trace(fname):
            return
        count = 1.0
        lineno = frame.f_lineno
        read_something = False
        try:
            with open(Scalene.free_signal_filename, "r") as f:
                for l, count_str in enumerate(f, 1):
                    read_something = True
                    count_str = count_str.rstrip()
                    count = float(count_str)
                    Scalene.memory_free_samples[fname][lineno] += count
                    # print(str(lineno) + " - SCALENE (" + str(l) + ") : free = " + str(count) + ", " + str(Scalene.memory_free_samples[fname][lineno]))
                    Scalene.total_memory_free_samples += count
                    Scalene.current_footprint -= count
                    # print("free " + str(count))
            if Scalene.current_footprint < 0:
                # In principle, this should not happen, but with sampling, it's _possible_, so we handle it here.
                Scalene.current_footprint = 0
            os.remove(Scalene.free_signal_filename)
        except Exception as e:
            # print(e)
            pass
        if read_something:
            Scalene.memory_free_count[fname][lineno] += 1
        return

    @staticmethod
    def alloc_event_signal_handler(_, frame):
        Scalene.malloc_signal_handler(True, frame)
        Scalene.free_signal_handler(True, frame)
    

    @staticmethod
    @lru_cache(128)
    def should_trace(filename):
        """Return true if the filename is one we should trace."""
        # Profile anything in the program's directory or a child directory,
        # but nothing else.
        if filename[0] == '<':
            # Don't profile Python internals.
            return False
        if 'scalene.py' in filename:
            # Don't profile the profiler.
            return False
        filename = os.path.abspath(filename)
        return Scalene.program_path in filename

    @staticmethod
    def start():
        """Initiate profiling."""
        os.chdir(Scalene.program_path)
        Scalene.enable_signals()
        Scalene.elapsed_time = Scalene.gettime()

    @staticmethod
    def stop():
        """Complete profiling."""
        Scalene.disable_signals()
        Scalene.elapsed_time = Scalene.gettime() - Scalene.elapsed_time
        os.chdir(Scalene.original_path) 

    @staticmethod
    @contextmanager
    def file_or_stdout(file_name):
        """Returns a file handle for writing; if no argument is passed, returns stdout."""
        # from https://stackoverflow.com/questions/9836370/fallback-to-stdout-if-no-file-name-provided
        if file_name is None:
            yield sys.stdout
        else:
            with open(file_name, 'w') as out_file:
                yield out_file

    @staticmethod
    def output_profiles():
        """Write the profile out (currently to stdout)."""
        # If we've collected any samples, dump them.
        if Scalene.total_cpu_samples == 0 and Scalene.total_memory_malloc_samples == 0 and Scalene.total_memory_free_samples == 0:
            # Nothing to output.
            return False
        
        # If I have at least one memory sample, then we are profiling memory.
        did_sample_memory = (Scalene.total_memory_free_samples + Scalene.total_memory_malloc_samples) > 1
        # Collect all instrumented filenames.
        all_instrumented_files = list(set(list(Scalene.cpu_samples_python.keys()) + list(Scalene.memory_free_samples.keys()) + list(Scalene.memory_malloc_samples.keys())))
        with Scalene.file_or_stdout(Scalene.output_file) as out:
            for fname in sorted(all_instrumented_files):

                this_cpu_samples = sum(Scalene.cpu_samples_c[fname].values()) + sum(Scalene.cpu_samples_python[fname].values())

                try:
                    percent_cpu_time = 100 * this_cpu_samples / Scalene.total_cpu_samples
                except ZeroDivisionError:
                    percent_cpu_time = 0

                # percent_cpu_time = 100 * this_cpu_samples * Scalene.mean_signal_interval / Scalene.elapsed_time
                print("%s: %% of CPU time = %6.2f%% out of %6.2fs." % (fname, percent_cpu_time, Scalene.elapsed_time), file=out)
                print("  \t | %9s | %9s | %s %s " % ('CPU %', 'CPU %', 'Avg memory  |' if did_sample_memory else '', 'Memory      |' if did_sample_memory else ''), file=out)
                print("  Line\t | %9s | %9s | %s%s [%s]" % ('(Python)', '(native)', 'growth (MB) |' if did_sample_memory else '', ' usage (%)   |' if did_sample_memory else '', fname), file=out)
                print("-" * 80, file=out)

                with open(fname, 'r') as source_file:
                    for line_no, line in enumerate(source_file, 1):
                        line = line.rstrip() # Strip newline
                        # Prepare output values.
                        n_cpu_samples_c = Scalene.cpu_samples_c[fname][line_no]
                        # Correct for negative CPU sample counts.
                        # This can happen because of floating point inaccuracies, since we perform subtraction to compute it.
                        if n_cpu_samples_c < 0:
                            n_cpu_samples_c = 0
                        n_cpu_samples_python = Scalene.cpu_samples_python[fname][line_no]
                        # Compute percentages of CPU time.
                        if Scalene.total_cpu_samples != 0:
                            n_cpu_percent_c = n_cpu_samples_c * 100 / Scalene.total_cpu_samples
                            n_cpu_percent_python = n_cpu_samples_python * 100 / Scalene.total_cpu_samples
                        else:
                            n_cpu_percent_c = 0
                            n_cpu_percent_python = 0
                        # Now, memory stats.
                        n_free_mb = (Scalene.memory_free_samples[fname][line_no] * Scalene.free_sampling_rate) / (1024 * 1024)
                        n_free_count = Scalene.memory_free_count[fname][line_no]
                        n_avg_free_mb = 0 if n_free_count == 0 else n_free_mb / n_free_count
                        
                        n_malloc_mb = (Scalene.memory_malloc_samples[fname][line_no] * Scalene.malloc_sampling_rate) / (1024 * 1024)
                        n_malloc_count = Scalene.memory_malloc_count[fname][line_no]
                        n_avg_malloc_mb = 0 if n_malloc_count == 0 else n_malloc_mb / n_malloc_count
                        
                        n_growth_mb = 0 if n_malloc_count == 0 and n_free_count == 0 else n_avg_malloc_mb # - n_avg_free_mb
                        n_drop_mb = 0 if n_malloc_count == 0 and n_free_count == 0 else n_avg_free_mb
                        n_usage_mb = 0 if Scalene.total_memory_malloc_samples == 0 else Scalene.memory_malloc_samples[fname][line_no] / Scalene.total_memory_malloc_samples

                        # Finally, print results.
                        n_cpu_percent_c_str = "" if n_cpu_percent_c == 0 else '%6.2f%%' % n_cpu_percent_c
                        n_cpu_percent_python_str = "" if n_cpu_percent_python == 0 else '%6.2f%%' % n_cpu_percent_python
                        n_growth_mb_str  = "" if (n_growth_mb == 0 and n_usage_mb == 0) else '%11.0f' % n_growth_mb
                        # n_usage_mb_str  = "" if n_usage_mb == 0 else '%9.2f%%' % (100 * n_usage_mb)
                        n_usage_mb_str  = "" if n_drop_mb == 0 else '%11.0f' % n_drop_mb
                        if did_sample_memory:
                            print("%6d\t | %9s | %9s | %11s | %11s | %s" %
                                  (line_no, n_cpu_percent_python_str, n_cpu_percent_c_str, n_growth_mb_str, n_usage_mb_str, line), file=out)
                        else:
                            print("%6d\t | %9s | %9s | %s" %
                                  (line_no, n_cpu_percent_python_str, n_cpu_percent_c_str, line), file=out)
                    print("", file=out)
                    return True


    @staticmethod
    def disable_signals():
        """Turn off the profiling signals."""
        try:
            signal.signal(Scalene.cpu_timer_signal, signal.SIG_IGN)
        except Exception as ex:
            pass
        signal.signal(Scalene.malloc_signal, signal.SIG_IGN)
        signal.signal(Scalene.free_signal, signal.SIG_IGN)
        signal.setitimer(Scalene.cpu_timer_signal, 0)

    @staticmethod
    def exit_handler():
        """When we exit, disable all signals."""
        Scalene.disable_signals()

    @staticmethod
    def main():
        """Invokes the profiler from the command-line."""
        usage = dedent("""Scalene: a high-precision CPU and memory profiler.
            https://github.com/emeryberger/Scalene

                for CPU profiling only:
            % python -m scalene yourprogram.py
                for CPU and memory profiling (Mac OS X):
            % DYLD_INSERT_LIBRARIES=$PWD/libscalene.dylib PYTHONMALLOC=malloc python -m scalene yourprogram.py
                for CPU and memory profiling (Linux):
            % LD_PRELOAD=$PWD/libscalene.so PYTHONMALLOC=malloc python -m scalene yourprogram.py
            """)
        parser = argparse.ArgumentParser(prog='scalene', description=usage, formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument('prog', type=str, help='program to be profiled')
        parser.add_argument('-o', '--outfile', type=str, default=None, help='file to hold profiler output (default: stdout)')
        parser.add_argument('--profile-interval', type=float, default=float("inf"), help='output profiles every so many seconds.')
        parser.add_argument('--wallclock', dest='wallclock', action='store_const', const=True, default=False, help='use wall clock time (default: virtual time)')
        # Parse out all Scalene arguments and jam the remaining ones into argv.
        # See https://stackoverflow.com/questions/35733262/is-there-any-way-to-instruct-argparse-python-2-7-to-remove-found-arguments-fro
        args, left = parser.parse_known_args()
        sys.argv = sys.argv[:1]+left
        Scalene.set_timer_signal(args.wallclock)
        Scalene.output_profile_interval = args.profile_interval
        Scalene.next_output_time = Scalene.gettime() + Scalene.output_profile_interval
        try:
            with open(args.prog, 'rb') as prog_being_profiled:
                Scalene.original_path = os.getcwd()
                # Read in the code and compile it.
                code = compile(prog_being_profiled.read(), args.prog, "exec")
                # Push the program's path.
                program_path = os.path.dirname(os.path.abspath(args.prog))
                sys.path.insert(0, program_path)
                Scalene.program_path = program_path
                # os.chdir(program_path)
                # Set the file being executed.
                the_globals['__file__'] = args.prog
                Scalene.output_file = args.outfile
                # Start the profiler.
                profiler = Scalene(os.path.join(program_path, os.path.basename(args.prog)))
                try:
                    profiler.start()
                    # Run the code being profiled.
                    exec(code, the_globals)
                    profiler.stop()
                    # Go back home.
                    # os.chdir(Scalene.original_path)
                    # If we've collected any samples, dump them.
                    if profiler.output_profiles():
                        pass
                    else:
                        print("Scalene: Program did not run for long enough to profile.")
                except Exception as ex:
                    template = "Scalene: An exception of type {0} occurred. Arguments:\n{1!r}"
                    message = template.format(type(ex).__name__, ex.args)
                    print(message)
                    print(traceback.format_exc())
        except (FileNotFoundError, IOError):
            print("Scalene: could not find input file.")

Scalene.main()
