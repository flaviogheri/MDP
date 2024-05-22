#!/usr/bin/env python

import rospy
import smach
import smach_ros
import yaml
import subprocess

import threading # (required for task monitoring)

# Load paths from YAML file
with open('paths.yml', 'r') as file:
    paths = yaml.safe_load(file)['external_paths']

with open('global_var.yml', 'r') as file:
    global_var = yaml.safe_load(file)['FSM_var']

# ---------------- State Classes -------------

"""
Things to do: 

Actually Create the Scripts for the different States

Actually Ask what data should the StateTree transfer to the different state, do i transfer the map ?

Wont i need to read that continuosly anyways ? (in RobotMonitoring), hence handeled in seperate node ?


Also reflect FSM will be a node, hence treat this as a node and nothing else...

Therefore, where to save the paths ?-> Should these be within the FSM node or within respective packages ?


Maybe do research from other projects ?


TODO : 

> change all the scripts so that they are defined correct

> Finish the ST in the main section

> make sure the logic flows correctly

> 










"""














class Initialization(smach.State):
    def __init__(self):
        smach.State.__init__(self,
                              outcomes=['map_needed', 'map_exists'],
                              output_keys=['map_data'])

    def execute(self, userdata):
        # checks if map already available
        
        if global_var['MAP_AVAILABILITY']=='1':
            return 'map_exists'
        else:
            return 'map_needed'
    
class ProcessMap(smach.State):
    def __init__(self):
        smach.State.__init__(self,
                              outcomes=['map_created', 'map_failed'],
                              output_keys=['map_data'])

    def execute(self, userdata):
        if userdata.map_available: #checking input key
            rospy.loginfo("Using existing map")
            return 'map_created'
        else:
            # Process the received map data
            subprocess.run(['python3', paths['process_map_data']], check=True)
            return 'map_created'
        except Exception as e:  # Catch potential errors in processing
            rospy.logerr(f"Error processing map: {e}")
            return 'map_failed'
        
class GenerateGlobalPath(smach.State):
    def __init__(self):
        smach.State.__init__(self,
                              outcomes=['path_plans_generated', 'planning_failed'],
                              input_keys=['map_data'],
                              output_keys=['general_waypoints'])

    def execute(self, userdata):
        try:
            # Use map data to generate global cleaning paths (e.g., using a path planning algorithm)
            subprocess.run(['python3', paths['generate_global_paths']], check=True)
            return 'path_plans_generated'
        except Exception as e:
            rospy.logerr(f"Error generating paths: {e}")
            return 'planning_failed'

class AssignTasks(smach.State):
    def __init__(self):
        smach.State.__init__(self,
                              outcomes=['tasks_assigned'],
                              input_keys=['general_waypoints'],
                              output_keys=['waypoint_lists'])

    def execute(self, userdata):
        subprocess.run(['python3', paths['assign_tasks_to_robots']], check=True)
        return 'tasks_assigned'
    
        # except Exception as e:  # Catch communication errors or other failures
        #     rospy.logerr(f"Error assigning tasks: {e}")
        #     return 'loss_comm' 
        

class RobotMonitoring(smach.State):
    def __init__(self):
        smach.State.__init__(self,
                              outcomes=['tasks_complete', 'home_request'],
                              input_keys=['waypoint_lists'],
                              output_keys=['remap_request'])

    def execute(self, userdata):


############################ Main Execution Logic ##################


if __name__== '__main__':
    rospy.init_node('robot_state_machine')


    sm = smach.StateMachine(outcomes=['END'])

    with sm: 
        smach.StateMachine.add()



##################### Processing the data is done in contemporary to robot.... ############
  
# class AwaitMapData(smach.State):
#     def __init__(self):
#         smach.State.__init__(self, outcomes=['map_received', 'lost_connection'])
#         self.map_data_received = False

#     def execute(self, userdata):
#         while not self.map_data_received:
#             # Check for map data on a ROS topic or service
#             # ...

#             if map_data_is_valid:
#                 self.map_data_received = True
#                 return 'map_received'
            
#             rospy.sleep(1)  # Sleep for a short duration to avoid blocking

#         return 'lost_connection'  # Timeout or invalid data


########### Need to change part below ######
""" I think the part below needs to be changed as GUI isnt a state etc..

Would change this all into a `RobotMonitoring` state. Where these different subsections
are achieved.

"""



# class LocateRobot(smach.State):
#     def __init__(self):
#         smach.State.__init__(self, outcomes=['location_updated', 'location_error'])
    
#     def execute(self, userdata):
#         try:
#             # Get robot's LiDAR data
#             lidar_data = get_lidar_data()  # Use ROS topic/service to retrieve data
#             # Process LiDAR data to determine the robot's location (e.g., using SLAM)
#             robot_location = process_lidar_data(lidar_data) 
#             # Update the robot's location in the server's data structure
#             update_robot_location(robot_location)
#             return 'location_updated'
#         except Exception as e:
#             rospy.logerr(f"Error locating robot: {e}")
#             return 'location_error'
        
# class GUI(smach.State):
#     def __init__(self):
#         smach.State.__init__(
#             self,
#             outcomes=[
#                 "tasks_completed",
#                 "task_failed",
#                 "loss_comm",
#                 "path_change",
#                 "remap_needed",
#                 "GUI",  # if nothing is triggered, stays in this state
#             ],
#             input_keys=[
#                 "task_status",
#                 "robot_status",
#                 "location_updated",
#                 "location_error",
#             ],
#             output_keys=["new_path", "remap_request"],
#         )

#     def execute(self, userdata):
#         # Check for task and robot status
#         if userdata.task_status == "completed":
#             return "tasks_completed"
#         elif userdata.task_status == "failed":
#             return "task_failed"
#         elif userdata.robot_status == "disconnected":
#             return "loss_comm"
        
#         # Check for location updates or errors
#         if userdata.location_updated:
#             # Update the GUI with the new robot location
#             update_gui_with_location(userdata.location_updated)  # You'll need to implement this function
#         elif userdata.location_error:
#             # Handle the location error, e.g., display an error message in the GUI or try to recover
#             handle_location_error(userdata.location_error) # You'll need to implement this function

#         # Check for user input/updates (new path, remap request)
#         # ... (same as in your original code)

#         # If no transitions were triggered, stay in the GUI state
#         return "GUI"
        

# class ErrorHandling(smach.State):
#     def __init__(self):
#         smach.State.__init__(self, outcomes=['resume_tasks', 'map_needed'])

#     def execute(self, userdata):
#         # Implement error handling logic based on the specific error type
#         error_type = get_error_type()
#         if error_type == "robot_failure":
#             handle_robot_failure()
#             return 'resume_tasks'  # Try to resume tasks if possible
#         elif error_type == "map_failure":
#             return 'map_needed'  # Trigger re-mapping
