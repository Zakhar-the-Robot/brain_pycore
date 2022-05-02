#!/usr/bin/env python3
# *************************************************************************
#
# Copyright (c) 2022 Andrei Gramakov. All rights reserved.
#
# site:    https://agramakov.me
# e-mail:  mail@agramakov.me
#
# *************************************************************************

import sys
import importlib

if importlib.find_loader('rospy') is None:
    sys.path.append("/opt/ros/noetic/lib/python3/dist-packages")
    if not  importlib.find_loader('rospy'):
        raise ImportError("Coulnd find rospy check your ROS version! (Supported: Noetic)")
    
