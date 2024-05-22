## Why SMACH

Smach was used as it is an easy way to create a working FSM with ROS on Python.

> Commonly used within the ROS community


# FSM of Server and Individual Robot



## Server FSM

Initialization --> MapAcquisition --> PathPlanning --> TaskAssignment --> RobotMonitoring

### Server States: 

> Initialization - Initialize connection to robots
    - Outcomes: map_needed (if no map available), map_available

> MapAcquisition - generate map of environment
    - Substates: 
        > AwaitMapData - Wait for robot to provide map data
            - Outcomes : recieved_map, lost_connection
        > ProcessMap - Process map data 
            - Outcomes : map_created, map_failed

> PathPlanning - create robot paths
    - Substates: 
        > GenerateGlobalPath - Seperate maps/coordinate different trajectories for robot cleaning
         - Outcomes: path_plans_generated, planning_failed 

> TaskAssignment - Assign tasks to robots
    - Substates: 
        > AssignTasks - Assign tasks to all robots
            - Outcomes : tasks_assigned, loss_comm 


Need to change the part below, should all be part of one State: "RobotMonitoring"...

        > GUI - Monitor Progress and display to user
            - Outcomes: tasks_completed, task_failed, loss_comm, path_change, remap_needed 

> Localization - Update Location of robots
    > LocateRobot - Retrieves Lidar data and returns robot location 
        - Outcomes: location_updated, location_error

> ErrorHandling - Handle any errors in robots