import threading
import time

# Task class with priority and execution tracking
class Task:
    # task initialization
    def __init__(self, name, priority, duration):
        self.name = name # task name
        self.priority = priority # task priority
        self.duration = duration # run duration
        self.wait_time = 0 # how long the task has waited
        self.has_run = False # whether the task has run

    # method to run the task
    def run(self):
        print(f"[{self.name}] Running with priority {self.priority}") # log start
        time.sleep(self.duration) # sleep to force simultaneous execution
        print(f"[{self.name}] Finished") # log finish
        self.has_run = True

# Scheduler to track when tasks have been executed
class Scheduler:
    # intitialize scheduler
    def __init__(self, tasks, enable_aging=True, max_cycles=25):
        self.todo = tasks[:] # tasks that need to be executed
        self.completed = []  # tasks that have been executed
        self.enable_aging = enable_aging # boolean to turn aging on/off for demo
        self.cycle_count = 0 # how many iterations through todo list
        self.max_cycles = max_cycles # max iterations before stop

    # method to start scheduler
    def start(self):
        try:
            while self.todo: # while there are unexecuted tasks
                if self.cycle_count >= self.max_cycles: # if we have reached max iterations
                    print("\n[Scheduler] Reached cycle limit. Starvation occurred.") 
                    break # stop the loop

                # sort tasks that need to be executed
                self.todo.sort(key=lambda t: t.priority)

                # always run highest priority first
                task = self.todo[0]

                # run the task
                t = threading.Thread(target=task.run) # create thread
                t.start() # start thread
                t.join() # join thread to prevent main thread continuation

                # only move lists when aging is on, or theyre low/med priority
                # to simulate starvation    
                if self.enable_aging or task.name != "HighPriority":
                    self.todo.remove(task) # after executing, remove from todo
                    self.completed.append(task) # add to completed

                # apply aging to tasks to prevent starvation
                if self.enable_aging:
                    for tsk in self.todo: # if the task still needs execution
                        tsk.wait_time += 1 # increase wait time by 1
                        if tsk.wait_time >= 3: # when wait time becomes more than 3
                            tsk.priority -= 1  # increase task priority
                            tsk.wait_time = 0 # reset wait time
                            print(f"[{tsk.name}] Aging applied. New priority: {tsk.priority}")

                self.cycle_count += 1 # count cycles (incr here)
                time.sleep(0.1)  # sleep for slight delay

            # after todo is empty, end loop
            if not self.todo:
                print(f"\n[Scheduler] All tasks completed in {self.cycle_count} cycles.")
        except KeyboardInterrupt:
            print(f"\n[Scheduler] Interrupted after {self.cycle_count} cycles.")

if __name__ == "__main__":
    tasks = [
        Task("HighPriority", priority=1, duration=1),
        Task("MedPriority", priority=3, duration=1),
        Task("LowPriority-1", priority=5, duration=1),
        Task("LowPriority-2", priority=5, duration=1),
    ]

    print("\n=== Running with Aging Enabled ===")
    scheduler = Scheduler(tasks, enable_aging=True, max_cycles=25)

    # print("\n=== Running with Aging Disabled ===")
    # scheduler = Scheduler(tasks, enable_aging=False, max_cycles=25)
    scheduler.start()
