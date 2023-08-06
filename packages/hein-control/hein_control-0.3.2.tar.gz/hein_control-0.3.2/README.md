# Hein Experiment Control

`hein_control` is a collection of code for automating and scheduling tasks related to experiment monitoring. The 
Experiment Scheduler module (`hein_control.scheduler`) contains code for scheduling actions at given time spacing 
with a focus on reaction monitoring.  

## Experiment Scheduler 

This repository contains code for "Experiment Schedulers" which will perform "actions" (Python functions) at user-defined 
time points. This package has no dependencies beyond the Python standard library. 

For example, performing the function `perform_sampling_sequence` 5 times at 60 second intervals then 10 
times at 300 second intervals. At the moment, action functions are user-defined, but a planned feature is to have built-in
methods for standard operations like direct-inject sequences. An example script has been provided to illustrate basic 
usage (please see `example_scheduler_script.py`). 

### Current workflow: 
1) The user defines action function(s) to perform
2) The `SamplingScheduler` is instantiated, providing those functions in the order they are to be executed 
3) Time points are added with one of: 

    a) `.insert_time_point`: inserts a single time point
    b) `.insert_time_point_list`: inserts a list of time points
    c) or `.insert_time_point_list_pairs`: inserts a sequence of time point list pairs (e.g. 6 times 60 seconds, then 
       10 times 120 seconds, etc.)
    
4) The `SamplingScheduler` sequence is started with `SamplingScheduler.start_sequence()`

### Notes
- A running `SamplingScheduler` instance may be paused with `SamplingScheduler.pause_sequence()`
- A `SamplingScheduler` instance may be manually triggered at any time (a time point is automatically created with its 
  associated metadata)
- When executing in a script, `SamplingScheduler.join()` should be placed at the end of the script to prevent 
    premature exit. 

### Modules and Classes

#### Actions

The `action.SchedulerAction` class represents callable functions with default arguments and keyword arugments for calling. 
"Action" methods (any callable) are registered with `SchedulerAction.register_action(callable)` and may then be associated with any 
Scheduler instance. 

The `action.TrackedAction` class wraps the above class to handle execution and storage of runtime metadata: 
 - `.time_started`: time when the action was started
 - `.time_completed`: time when the action was completed
 - `.started_timestamp`: `datetime.datetime` timestamp for when the action was started
 - `.action_duration`: duration of the action
 - `.name`: action name
 - `.status`: string status of the action execution
 - `.method_return`: any return from the method upon completion 

#### Time Points

There are two classes in the `.timepoint` module: `TimePoint` and `ActionTimePoint`. The former is for denoting that an 
action occurred at a given time, and the latter is for managing a sequence of actions at a given time. Any number of 
actions may be associated with an `ActionTimePoint` instance and they will be performed in the order provided. A variety 
of properties are available for retrieving metadata associated with the actions of a time point.  

Time points are triggered by either calling the class instance or by calling `.trigger()`. Keyword argument 
passthrough is supported, but has some restrictions as the keywords must be provided as dictionaries keyed by their 
respective function names. 

