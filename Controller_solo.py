#!/usr/bin/env python


#####	Import Libraries	#####
import rospy
import sys
import serial
import struct
import xml.etree.ElementTree as ET
import math
import signal
import time

from US2066 import US2066Base as DISP
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from std_msgs.msg import String, Char, Float64, Int32

#####	Define Functions	#####

#####	Reset the OLED cursor to the first line and write out the string "Temperature:"	#####
#def oled_init(display):
#  display.command(0x01)
#  display.command(0x00)
#  display.write("Temperature:")
 
#####	Move the OLED cursor to the second line and write out the temperature	#####	
#def oled_temp(display, temperature):
#  display.command(0xA0)
#  display.write(temperature)

#####	Read the serial port, write incoming temperature data into an .xml file, parse the .xml file, obtain the temperature data	#####
#def read_temp(tempOldSerialData):
#	tempXmlTemplate = open("temp_xml_template.xml", 'r+')
#	tempXmlBackup = tempXmlTemplate.read()
#	tempXmlBackup2 = open("temp_xml_backup.xml", 'w+')
#	tempCover = tempXmlBackup2.write(tempXmlBackup)
#	tempXmlTemplate.close()
#	tempXmlBackup2.close()

#	tempXmlData = open("temp_xml_data.xml", 'w+')
#	tempSerialData = ser.readline()
#	if tempSerialData:
#		tempXmlBackup = open("temp_xml_backup.xml", 'w+')
#		tempXmlBackup.write(tempSerialData)
#		tempOldSerialData = tempSerialData
#		tempXmlBackup.close()
#	if not tempSerialData:
#		tempSerialData = tempOldSerialData

#	tempXmlData.write(tempSerialData)

#	tempXmlData.close()
#	time.sleep(0.01)
		
#	tempXmlTree = ET.parse("temp_xml_data.xml")
#	tempXmlRoot = tempXmlTree.getroot()

#	temp = tempXmlRoot[0][0].text

#	return temp

#####	Initialization	#####

#####	I2C address of OLED Display	#####
#disp = DISP(0x3C)

#####	Resets OLED, Clears OLED, Initializes OLED, then waits 10ms	#####
#disp.begin()
#time.sleep(0.01)

#####	Start up OLED by sending I2C address to "oled_init" function, then wait 1ms	#####
#oled_init(disp)
#time.sleep(0.001)

#####	Open the .xml template in read-only mode, assign whatever is inside to the tempOldSerialData variable, then close the file	#####
#tempOldSerialInit = open("temp_xml_template.xml", 'r+')
#time.sleep(0.01)
#tempOldSerialData = tempOldSerialInit.read()
#time.sleep(0.01)
#tempOldSerialInit.close()
#time.sleep(0.01)

#####	Create the arrays that will be sent over the serial port, populate them with arbitrary data	#####
#axesArray = [1.0,1.0,1.0,1.0]
#buttonArray = [1.0, 1.0, 1.0, 1.0]
#axesArray = []
#buttonArray = []

#####	Define the serial port and baud rate	#####
ser = serial.Serial('/dev/ttyO4', 38400)

#####	Populate the two arrays with data from the Xbox 360 controller	#####
#while True:

def callback(data):
	#axesArray = [1.0,1.0,1.0,1.0]
	#buttonArray = [1.0, 1.0, 1.0, 1.0]
	print "callback"
	
	axesArray = []
	buttonArray = []
	
	#####	Fill axesArray with the left analog stick's x & y axes, as well as the right analog stick's x & y axes, then cut off the arbitrary data	#####
	axesArray.insert(0,data.axes[0])
	axesArray.insert(1,data.axes[1])
	axesArray.insert(2,data.axes[3])
	axesArray.insert(3,data.axes[4])
#	axesArray=axesArray[:-4]

	#####	Fill buttonArray with the D-Pad's left/right/up/down data, then cut off the arbitrary data	#####
	buttonArray.insert(0,data.buttons[11])
	buttonArray.insert(1,data.buttons[12])
	buttonArray.insert(2,data.buttons[13])
	buttonArray.insert(3,data.buttons[14])
#	buttonArray=buttonArray[:-4]

	#####	Create the .xml structure	#####
	
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
	dPadUp.text = str(buttonArray[0])
	dPadDown.text = str(buttonArray[1])
	dPadLeft.text = str(buttonArray[2])
	dPadRight.text = str(buttonArray[3])

	#####	Package everything together, store it in the variable "myData"	#####
	myData = ET.tostring(controllerPacket)
	
	#####	Send info through the serial port, along with a newline character (required for ROV to read data properly)	#####
	ser.write(myData)
	ser.write('\n')

	#####	Print both arrays to the terminal (for debugging purposes, won't be visible in standard usage)	#####
	print "AXES:"
	print axesArray
	print "BUTTONS:"
	print buttonArray
	

#####	Read the data coming from the Xbox 360 controller, located at /dev/input/js0	#####
def readXbox():
	#####	Create a ROS node called "readXbox", make it unique by setting anonymous to false (won't append random numbers to the end of the node name)	#####
	rospy.init_node('readXbox',anonymous=False)
	
	#####	Subscribe to the "joy" topic, which uses message type "Joy", and set the data to the variable "callback"	#####
	print "readXbox"
	
	rospy.Subscriber("joy",Joy,callback)
	#testStuff = rospy.Subscriber("joy",Joy)
	#callback(testStuff,axesArray,buttonArray)

	#####	Create a topic called "axes" for other nodes to read the custom data packet (won't be used, since no other node is talking to it)	#####
	#pubAxes = rospy.Publisher("axes",String,queue_size=10)

	#####	Keep python from exiting until this node is stopped	##### 
	rospy.spin()

#####	Go to the function that reads the serial port for temperature data, set that data to the variable "temp"	#####
#temp = read_temp(tempOldSerialData)

#####	Print the temperature value to the terminal (for debugging purposes, won't be visible in standard usage)	#####
#print(temp)

#####	Write the temperature (variable "temp") to the OLED Display (at I2C address "disp"), wait 10ms	#####
#oled_temp(disp, temp)
#time.sleep(0.01)

#####	Allows the script to be executed by passing it as a command to the Python interpreter (allows user to say "python Controller_solo.py" in terminal), executes at beginning	#####



if __name__=='__main__':
	#####	Perform the readXbox function	#####
	readXbox()
	
while True:
	print "AAAAA"


#####	Checks if Ctrl-C was pressed, kills the program if it was	#####
#def signal_handler(signal, frame):
#	print('Exiting...')
#	sys.exit(0)

#####	Checks if Ctrl-C was pressed also, backup in case the function above doesn't work	#####
#signal.signal(signal.SIGINT, signal_handler)

