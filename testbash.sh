#!/bin/bash

. ~/catkin_ws/devel/setup.bash

cd ~/catkin_ws/src/beginner_tutorials/scripts
rm -f Controller_solo_dynamic.py temp_xml_template.xml
cd ~
cp Controller_solo_dynamic.py temp_xml_template.xml catkin_ws/src/beginner_tutorials/scripts
cd ~/catkin_ws/src/beginner_tutorials/scripts
chmod +x Controller_solo_dynamic.py
cd ~

roslaunch launchjoy.launch


