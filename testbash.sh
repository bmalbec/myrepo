#!/bin/bash

. ~/catkin_ws/devel/setup.bash

roslaunch launchjoy.launch
cd ~
python Controller_solo.py

