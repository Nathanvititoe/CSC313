import threading
import time

# class to simulate a needed resource
class Resource:
    # initialize resource
    def __init__(self, name):
        self.name = name # resource name
        self.lock = threading.Lock() # resource lock

# Class for creating tasks that sim deadlock
class Task(threading.Thread):
    # task initialization
    def __init__(self, name, first_resource, second_resource):
        super().__init__()
        self.name = name # task name
        self.first = first_resource # resource needed by task
        self.second = second_resource # resource needed by task

    # method to run the task
    def run(self):
        print(f"{self.name} requesting {self.first.name}") # log request for first resource
        
        with self.first.lock: # req lock for first resource
            print(f"{self.name} allocated {self.first.name}") # log allocation of first resource
            time.sleep(1)  # small delay before next lock req

            print(f"{self.name} requesting {self.second.name}") # log request for second resource 
            with self.second.lock: # req lock for first resource
                print(f"{self.name} allocated {self.second.name}") # log allocation of second resource

# function to sim deadlock by forcing resource pickup out of order
def simulate_deadlock():
    t1 = Task("Thread-1", resource_A, resource_B) # t1 picks up a->b
    t2 = Task("Thread-2", resource_B, resource_A) # t2 picks up b->a

    t1.start() # start thread 1
    t2.start() # start thread 2
    t1.join() # join thread 1
    t2.join() # join thread 2


# function to fix deadlock by requiring a consistent order, similar to dining philosophers
def ordering_fix():
    # both threads pick up resources in order
    t1 = Task("Thread-1", resource_A, resource_B)
    t2 = Task("Thread-2", resource_A, resource_B)

    t1.start() # start thread 1
    t2.start() # start thread 2
    t1.join() # join thread 1
    t2.join() # join thread 2

if __name__ == "__main__":
    resource_A = Resource("Resource A")
    resource_B = Resource("Resource B")

    # simulate_deadlock() # run to sim deadlock
    ordering_fix() # run to show prevention of deadlock
