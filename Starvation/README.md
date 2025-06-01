Starving can be prevented by using aging to slowly increase the priority of low priority tasks. This way, eventually they will become high priority and the scheduler will have to run them. 

In my starvation simulation you can see that without the aging enabled, the tasks get stuck running only high priority items, but once aging is applied and low priority items become high priority after waiting for resources for awhile, all items are run fairly quickly. 

In code, I used aging to avoid starvation by applying a wait time to each task instance, and whenever that task was skipped, the wait time would increase. 
If a task's wait time got to 3, it would increase the priority of that task by 1. 

This solution ensures that even low priority tasks will eventually be reached by the scheduler.