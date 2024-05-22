#!/usr/bin/env python 


import rospy 
import smach
import smach_ros

# Main Robot States

class MappingEnv(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['map_created', 'map_failed'])
    
    def execute(self, userdata):
        if map==created:
            return 'map_created'

        elif map!=created: 
            # returns that map failed (server will change which robot
            # is the primary accordingly (use other robot to map env ?))
            return 'map_failed'

class FollowPath(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['path_completed','no_path'])
    
    def execute(self, userdata):
        if path == blocked:
            return 'no_path'
        elif waypoints<0:
            return 'path_completed'

class GoToDockingStation(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['docking_success','docking_failed'])
    
    def execute(self, userdata):
        if docking==success:
            return 'docking_success'

class GoToLastWaypoint(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['waypoint_reached', 'waypoint_not_reached'])
    def execute(self, userdata):
        if waypoint==reached:
            return 'waypoint_reached'
        elif navigation==failed:
            return 'waypoint_not_reached'


# Other States

class Manual(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['no_connection', 'quit_connection'])
    
    def execute(self, userdata):
        if time>30:
            return 'no_connection'
        elif quit == pressed:
            return 'quit_connection'