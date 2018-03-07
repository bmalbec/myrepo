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

from US2066 import US2066Base as DISP
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from std_msgs.msg import String, Char, Float64, Int32


#####################################
#####	Define Functions	#####
#####################################

#####	Make the NT^2 logo	#####
def oled_logo(display):
	display.command(0x01)
	display.command(0x00)
	display.write("  !@%^(")
	display.command(0xA3)
	display.write("#$&*")

#####	Reset the OLED cursor to the first line and write out the string "Temperature:"	#####
def oled_init(display):
	###trying to display NT2 logo	###

	##################################
	display.command(0x01)
	display.command(0x00)
	display.write("Temperature:")
	
	###trying out###
	display.command(0x0C)
	####################

#####	Move the OLED cursor to the second line and write out the temperature	#####	
def oled_temp(display, temperature):
  	display.command(0xA0)
  	display.write(temperature)
	###trying out#######
	display.command(0xA6)
	####################
  	display.write(" ~C ")

def init_temp_values(tempXmlInitFile):
	tempXmlInit = open(tempXmlInitFile, 'r')	#open initialization xml for pwm values
	time.sleep(0.001)
	tempInitValues = tempXmlInit.read()		#read the initial pwm values into pwmInitValues
	time.sleep(0.001)
	tempXmlInit.close()						#close initialization xml
	time.sleep(0.001)

	tempXmlBackup = open('/home/ubuntu/temp_xml_backup.xml', 'w+')
	time.sleep(0.001)
	tempXmlBackup.write(tempInitValues)
	time.sleep(0.001)
	tempXmlBackup.close()

	return tempInitValues

#####	Read the serial port, write incoming temperature data into an .xml file, parse the .xml file, obtain the temperature data	#####
def read_temp():
	#tempXmlTemplate = open("temp_xml_template.xml", 'r')
	#tempXmlBackup = tempXmlTemplate.read()
	#tempXmlTemplate.close()
	time.sleep(0.001)
	tempXmlData = open('/home/ubuntu/temp_xml_data.xml', 'w+')

	tempSerialData = ser.readline()

	time.sleep(0.001)
	if tempSerialData:
		tempXmlBackup = open('/home/ubuntu/temp_xml_backup.xml', 'w+')
		tempXmlBackup.write(tempSerialData)
		tempOldSerialData = tempSerialData
		tempXmlBackup.close()
	if not tempSerialData:
		tempXmlBackup = open('/home/ubuntu/temp_xml_backup.xml', 'r')
		tempBackupData = tempXmlBackup.read()
		tempSerialData = tempBackupData
		tempXmlBackup.close()



	tempXmlData.write(tempSerialData)

	tempXmlData.close()
	time.sleep(0.001)

	tempXmlTree = ET.parse('/home/ubuntu/temp_xml_data.xml')
	tempXmlRoot = tempXmlTree.getroot()

	temp = tempXmlRoot[0][0].text

	return temp

#####	Populate the two arrays with data from the Xbox 360 controller	#####
def callback(data):

	#####	Initialize the arrays	#####
	axesArray = []
	buttonArray = []

	#####	Fill axesArray with the left analog stick's x & y axes, as well as the right analog stick's x & y axes, then cut off the arbitrary data	#####
	axesArray.insert(0,data.axes[0])
	axesArray.insert(1,data.axes[1])
	axesArray.insert(2,data.axes[3])
	axesArray.insert(3,data.axes[4])


	#####	Fill buttonArray with the D-Pad's left/right/up/down data, then cut off the arbitrary data	#####
	buttonArray.insert(0,data.buttons[11])
	buttonArray.insert(1,data.buttons[12])
	buttonArray.insert(2,data.buttons[13])
	buttonArray.insert(3,data.buttons[14])


	#############################################
	#####	Create the .xml structure	#####
	#############################################

	#####	Create the header (parent)	#####
	controllerPacket = ET.Element('frame')

	#####	Create the child, which will house all of the data	#####
	controllerData = ET.SubElement(controllerPacket, 'data')

	#####	Create spots for the analog stick values and D-Pad values, label them as "items"	#####
	leftAnalogX = ET.SubElement(controllerData, 'item')
	leftAnalogY = ET.SubElement(controllerData, 'item')
	rightAnalogX = ET.SubElement(controllerData, 'item')
	rightAnalogY = ET.SubElement(controllerData, 'item')
	dPadLeft = ET.SubElement(controllerData, 'item')
	dPadRight = ET.SubElement(controllerData, 'item')
	dPadUp = ET.SubElement(controllerData, 'item')
	dPadDown = ET.SubElement(controllerData, 'item')

	#####	Assign names for each item to identify them easily	#####
	leftAnalogX.set('name','Left_X')
	leftAnalogY.set('name','Left_Y')
	rightAnalogX.set('name','Right_X')
	rightAnalogY.set('name','Right_Y')
	dPadLeft.set('name','D_Left')
	dPadRight.set('name','D_Right')
	dPadUp.set('name','D_Up')
	dPadDown.set('name','D_Down')

	#####	Set the values of each item, type cast them to strings	#####
	leftAnalogX.text = str(axesArray[0])
	leftAnalogY.text = str(axesArray[1])
	rightAnalogX.text = str(axesArray[2])
	rightAnalogY.text = str(axesArray[3])
	dPadLeft.text = str(buttonArray[0])
	dPadRight.text = str(buttonArray[1])
	dPadUp.text = str(buttonArray[2])
	dPadDown.text = str(buttonArray[3])

	#####	Package everything together, store it in the variable "myData"	#####
	myData = ET.tostring(controllerPacket)

	#####	Send info through the serial port, along with a newline character (required for ROV to read data properly)	#####
	ser.write(myData)
	ser.write('\n')


	#####	Go to the function that reads the serial port for temperature data, set that data to the variable "temp"	#####

	temp = read_temp()

	#####	Print the temperature value to the terminal (for debugging purposes, won't be visible in standard usage)	#####
#	print(temp)

	#####	Write the temperature (variable "temp") to the OLED Display (at I2C address "disp"), wait 10ms	#####
	oled_temp(disp, temp)
	time.sleep(0.001)


	#####	Print both arrays to the terminal (for debugging purposes, won't be visible in standard usage)	#####
	#screen.addstr(0, 0, statement.format(temp, axesArray, buttonArray,getcwd()))
	
#	print "AXES:"
#	print axesArray
#	print "BUTTONS:"
#	print buttonArray



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

#####	Custom OLED character codes	#####
#leftBracketTop = [0x1f,0x10,0x10,0x10,0x10,0x10,0x10,0x10]
#leftBracketBottom = [0x10,0x10,0x10,0x10,0x10,0x10,0x10,0x1f]
#nTopLeft = [0x0,0x1e,0x1e,0x1b,0x1b,0x1b,0x19,0x19]
#nTopRight = [0x0,0x3,0x3,0x3,0x3,0x3,0x3,0x13]
#nBottomLeft = [0x19,0x18,0x18,0x18,0x18,0x18,0x18,0x0]
#nBottomRight = [0x13,0x13,0x1b,0x1b,0x1b,0xf,0xf,0x0]
#tTopLeft = [0x0,0x1f,0x1f,0x1,0x1,0x1,0x1,0x1]
#tTopRight = [0x0,0x1f,0x1f,0x10,0x10,0x10,0x10,0x10]
#tBottomLeft = [0x1,0x1,0x1,0x1,0x1,0x1,0x1,0x0]
#tBottomRight = [0x10,0x10,0x10,0x10,0x10,0x10,0x10,0x0]
#rightBracketTop = [0x1f,0x1,0x1,0x1,0x1,0x1,0x1,0x1]
#rightBracketBottom = [0x1,0x1,0x1,0x1,0x1,0x1,0x1,0x1f]
top1=[0x1f,0x10,0x17,0x17,0x16,0x16,0x16,0x16]
top2=[0x0,0x0,0x11,0x11,0x19,0x19,0x19,0x19]
top3=[0x0,0x0,0x17,0x17,0x11,0x11,0x11,0x11]
top4=[0x1f,0x1,0x1d,0x1d,0x11,0x11,0x11,0x11]
bottom1=[0x16,0x16,0x16,0x16,0x16,0x16,0x10,0x1f]
bottom2=[0x1d,0xd,0xd,0xd,0x7,0x7,0x0,0x0]
bottom3=[0x11,0x11,0x11,0x11,0x11,0x11,0x0,0x0]
bottom4=[0x11,0x11,0x11,0x11,0x11,0x11,0x1,0x1f]

Ntop1=[0x0,0x1e,0x1e,0x1b,0x1b,0x1b,0x19,0x19]
Ntop2=[0x0,0x3,0x3,0x3,0x3,0x3,0x3,0x13]
Nbot1=[0x19,0x18,0x18,0x18,0x18,0x18,0x18,0x0]
Nbot2=[0x13,0x13,0x1b,0x1b,0x1b,0xf,0xf,0x0]
Ttop1=[0x0,0xf,0xf,0x1,0x1,0x1,0x1,0x1]
Ttop2=[0x0,0x1f,0x1f,0x10,0x10,0x10,0x10,0x10]
Tbot1=[0x1,0x1,0x1,0x1,0x1,0x1,0x1,0x0]
Tbot2=[0x10,0x10,0x10,0x10,0x10,0x10,0x10,0x0]

#####	Define the serial port and baud rate	#####
ser = serial.Serial('/dev/ttyO4', 38400, timeout=0.05)

#####	I2C address of OLED Display	#####
disp = DISP(0x3C)

#####	Resets OLED, Clears OLED, Initializes OLED, then waits 10ms	#####
disp.begin()
time.sleep(0.001)

#####	Display NT^2 logo	#####

oled_logo(disp)
time.sleep(3)

#####	Start up OLED by sending I2C address to "oled_init" function, then wait 1ms	#####
oled_init(disp)
time.sleep(0.001)

#####	Open the .xml template in read-only mode, assign whatever is inside to the tempOldSerialData variable, then close the file	#####
init_temp_values('/home/ubuntu/temp_xml_template.xml')
time.sleep(0.001)


#############################
#####	Main loop	#####
#############################

#####	Allows the script to be executed by passing it as a command to the Python interpreter (allows user to say "python Controller_solo.py" in terminal), executes at beginning	#####
if __name__=='__main__':	
	#####	Perform the readXbox function	#####
	readXbox()


