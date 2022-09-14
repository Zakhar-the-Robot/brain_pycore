# *************************************************************************
#
# Copyright (c) 2022 Andrei Gramakov. All rights reserved.
#
# This file is licensed under the terms of the MIT license.
# For a copy, see: https://opensource.org/licenses/MIT
#
# site:    https://agramakov.me
# e-mail:  mail@agramakov.me
#
# *************************************************************************

import sys
import importlib
import warnings

# ROS support
if importlib.find_loader('rospy') is None:
    sys.path.append("/opt/ros/noetic/lib/python3/dist-packages")
    if importlib.find_loader('rospy'):
        from . import ros
    else:
        warnings.warn("Couldn't find rospy check your ROS version! (Supported: Noetic)."
                      " `ros` subpackage will not be imported!")
