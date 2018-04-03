#!/usr/bin/env python

#####################################
#####	Import Libraries	#####
#####################################

import rospy
import sys
import serial
import struct
import xml.etree.ElementTree as ET
import math
import signal
import time
import curses
from os import getcwd
from Adafruit_PCA9685 import PCA9685 as PWM

from US2066 import US2066Base as DISP
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from std_msgs.msg import String, Char, Float64, Int32


#####################################
#####	Define Functions	#####
#####################################
def servo_move(data, rate):
	
	if data.buttons[11] == 1:
		rate -= 1
	if data.buttons[12] == 1:
		rate += 1

	if rate < 1:
		rate = 1
	if rate > 10:
		rate = 10
	
	if data.buttons[13] == 1:
		if servoCur > servoMin:
			servoCur -= rate
			
	if data.buttons[14] == 1:
		if servoCur < servoMax:
			servoCur += rate
	
	if servoCur < servoMin:
		servoCur = servoMin
	if servoCur > servoMax:
		servoCur = servoMax
		
	return servoCur

#####	Populate the two arrays with data from the Xbox 360 controller	#####
def callback(data):

	servoCur = servo_move(data, rate)
	
	
			
	#####	Print both arrays to the terminal (for debugging purposes, won't be visible in standard usage)	#####
	screen.addstr(0, 0, statement.format(servoMax, servoMin, servoCur, rate))
	screen.refresh()

	pwm.set_pwm(7,0,servoCur)


#####	Read the data coming from the Xbox 360 controller, located at /dev/input/js0	#####
def readXbox():
	#####	Create a ROS node called "readXbox", make it unique by setting anonymous to false (won't append random numbers to the end of the node name)	#####
	rospy.init_node('readXbox',anonymous=False)

	#####	Subscribe to the "joy" topic, which uses message type "Joy", and set the data to the variable "callback"	#####	
	rospy.Subscriber("joy",Joy,callback)

	#####	Create a topic called "axes" for other nodes to read the custom data packet (won't be used, since no other node is talking to it)	#####
	#pubAxes = rospy.Publisher("axes",String,queue_size=10)

	#####	Keep python from exiting until this node is stopped (this keeps the script alive)	##### 
	rospy.spin()


#####	Checks if Ctrl-C was pressed, kills the program if it was	#####
def signal_handler(signal, frame):
	print('Exiting...')
	sys.exit(0)

#####################################
#####	Initializations		#####
#####################################
pwm = PWM(0x40)

pwm.set_pwm_freq(485)

servoMin = 1300
servoMax = 4100
servoCur = servoMin
rate = 3

statement="""
Servo MINIMUM:{}
Servo MAXIMUM:{}
Servo CURRENT:{}
Servo RATE:{}

Press left/right on D-pad to decrease/increase opening/closing rate
Press 'A' to go into set-up mode

In set-up mode:
	Press 'X' to set current to new minimum
	Press 'Y' to set current to new maximum

*********************************************************************
*********************************************************************
*************				*****************************
*************	   Controller Servo	*****************************
*************	    	Demo		*****************************
*************				*****************************
*********************************************************************
*********************************************************************
"""

screen = curses.initscr()

#############################
#####	Main loop	#####
#############################

#####	Allows the script to be executed by passing it as a command to the Python interpreter (allows user to say "python Controller_solo.py" in terminal), executes at beginning	#####
if __name__=='__main__':	
	#####	Perform the readXbox function	#####
	readXbox()

curses.endwin()
