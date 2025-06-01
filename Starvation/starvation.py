# this is a copy of main.py with starvation/priority queue logic added
import threading # allow multithreading
import time # allow time measurements
import cProfile # get cpu performance profile

# task class to add priorities to each thread
class Task:
# task constructor 
    def __init__(self, name, priority, duration):
        self.name = name # thread name
        self.priority = priority # thread priority
        self.duration = duration # thread duration
        self.wait_time = 0  # thread wait time (for aging)

    # method to run each thread
    def run(self):
        print(f"[{self.name}] Running with priority {self.priority}")
        time.sleep(self.duration) # sleep thread to force simultaneous running
        print(f"[{self.name}] Finished")

# scheduler class to sim locking
class Scheduler:
    def __init__(self, tasks):
        self.tasks = tasks # tasks
        self.lock = threading.Lock() # lock

    # method to start scheduler
    def start(self):
        # while there are tasks
        while self.tasks:
            # sort them by their priority
            self.tasks.sort(key=lambda t: t.priority)
            task = self.tasks.pop(0) # use the top of the list (highest prio)

            t = threading.Thread(target=task.run) # create thread and run it
            t.start() # start it 
            t.join() # join to prevent main thread execution

            # Aging step
            for tsk in self.tasks:
                tsk.wait_time += 1
                if tsk.wait_time >= 3:
                    tsk.priority = max(1, tsk.priority - 1)
                    tsk.wait_time = 0

if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()

    # Create task list with one high-priority thread and multiple low-priority ones
    tasks = [
        Task(name="HighPriority", priority=1, duration=1),
        Task(name="LowPriority-1", priority=10, duration=2),
        Task(name="LowPriority-2", priority=10, duration=2),
        Task(name="LowPriority-3", priority=10, duration=2),
    ]

    scheduler = Scheduler(tasks)
    scheduler.start()

    profiler.disable()
    profiler.dump_stats("main_thread.prof")

    
# # create worker thread
# def create_thread(name, duration):
#     print(f"[{name}] Starting, Duration: {duration}s") # log thread start
#     start_time = time.time() # get start time

#     # count to 10mil to sim cpu task
#     count = 0
#     for _ in range(10_000_000):
#         count += 1 # incr count by 1
 
#     time.sleep(duration) # sleep thread to force them to run simultaneously

#     end_time = time.time() # get end time

#     # output total duration
#     print(f"[{name}] Finished, Total Time: {end_time - start_time:.2f}s")

# # main logic flow
# def thread_control():
#     # init vars
#     sleep_durations = [1, 2, 3, 4, 5] # list of sleep durations   
#     threads = [] # init empty thread list

#     program_start = time.time() # get program start time

#     # loop through and create thread for each duration
#     for i, d in enumerate(sleep_durations):
#         # create one thread per duration index (pass name, duration)
#         t = threading.Thread(target=create_thread, args=(f"Thread-{i+1}", d))
#         threads.append(t) # append to threads list
#         t.start() # start thread

#     # block main thread until after all threads finish
#     for t in threads:
#         t.join()

#     program_end = time.time() # get end time
#     print(f"Completed ({program_end - program_start:.2f}s)") # log total duration

# # create profiler for main thread
# profiler = cProfile.Profile()
# profiler.enable()

# thread_control() # run main thread

# # remove profiler and log to file
# profiler.disable()
# profiler.dump_stats("main_thread.prof")
