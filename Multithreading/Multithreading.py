import threading # allow multithreading
import time # allow time measurements
import cProfile # get cpu performance profile

# create worker thread
def create_thread(name, duration):
    print(f"[{name}] Starting, Duration: {duration}s") # log thread start
    start_time = time.time() # get start time

    # count to 10mil to sim cpu task
    count = 0
    for _ in range(10_000_000):
        count += 1 # incr count by 1
 
    time.sleep(duration) # sleep thread to force them to run simultaneously

    end_time = time.time() # get end time

    # output total duration
    print(f"[{name}] Finished, Total Time: {end_time - start_time:.2f}s")

# main logic flow
def thread_control():
    # init vars
    sleep_durations = [1, 2, 3, 4, 5] # list of sleep durations   
    threads = [] # init empty thread list

    program_start = time.time() # get program start time

    # loop through and create thread for each duration
    for i, d in enumerate(sleep_durations):
        # create one thread per duration index (pass name, duration)
        t = threading.Thread(target=create_thread, args=(f"Thread-{i+1}", d))
        threads.append(t) # append to threads list
        t.start() # start thread

    # block main thread until after all threads finish
    for t in threads:
        t.join()

    program_end = time.time() # get end time
    print(f"Completed ({program_end - program_start:.2f}s)") # log total duration

# create profiler for main thread
profiler = cProfile.Profile()
profiler.enable()

thread_control() # run main thread

# remove profiler and log to file
profiler.disable()
profiler.dump_stats("main_thread.prof")
