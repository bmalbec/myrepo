#!/bin/bash

. ~/catkin_ws/devel/setup.bash

cd catkin_ws/src/beginner_tutorials/scripts
rm Controller_solo.py
cd ~

cp Controller_solo.py Controller_solo2.py
mv Controller_solo.py catkin_ws/src/beginner_tutorials/scripts
mv Controller_solo2.py Controller_solo.py

roslaunch launchjoy.launch


