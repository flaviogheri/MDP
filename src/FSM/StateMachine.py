#!/usr/bin/env python

import rospy
import smach

import smach_ros


# This is the Initial State Space



class StartRobot(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['map_exist','no_map'])
        # state init
        # understand if other robots are connected to server and therefore order itself

    def execute():
        # check if other robots are connected and if the map exists
        if xxx:
            return no
        
        else: 
            return outcome2

class slam_env(smach.State):
    def __init__():

    def execute():

class create_planning_trajectory(smach.State):
    def __init__(self, outcomes=[]):
        
    def execute():

