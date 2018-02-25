#!/usr/bin/env python

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

def oled_init(display):
  display.command(0x01)
  display.command(0x00)
  display.write("Temperature:")
  
def oled_temp(display, temperature):
  display.command(0xA0)
  display.write(temperature)
  
def read_temp(tempOldSerialData):
	tempXmlTemplate = open("temp_xml_template.xml", 'r+')
	tempXmlBackup = tempXmlTemplate.read()
	tempXmlBackup2 = open("temp_xml_backup.xml", 'w+')
	tempCover = tempXmlBackup2.write(tempXmlBackup)
	tempXmlTemplate.close()
	tempXmlBackup2.close()

	tempXmlData = open("temp_xml_data.xml", 'w+')
	tempSerialData = ser.readline()
	if tempSerialData:
		tempXmlBackup = open("temp_xml_backup.xml", 'w+')
		tempXmlBackup.write(tempSerialData)
		tempOldSerialData = tempSerialData
		tempXmlBackup.close()
	if not tempSerialData:
		tempSerialData = tempOldSerialData

	tempXmlData.write(tempSerialData)

	tempXmlData.close()
	time.sleep(0.01)
		
	tempXmlTree = ET.parse("temp_xml_data.xml")
	tempXmlRoot = tempXmlTree.getroot()

	temp = tempXmlRoot[0][0].text

	return temp

disp = DISP(0x3C)

disp.begin()

time.sleep(0.01)

oled_init(disp)
time.sleep(0.001)

tempOldSerialInit = open("temp_xml_template.xml", 'r+')
time.sleep(0.01)
tempOldSerialData = tempOldSerialInit.read()
time.sleep(0.01)
tempOldSerialInit.close()
time.sleep(0.01)

axesArray = [1.0,1.0,1.0,1.0]
buttonArray = [1.0, 1.0, 1.0, 1.0]
count=4

ser = serial.Serial('/dev/ttyO4', 38400)

while True:
	def callback(data):

		axesArray = [1.0,1.0,1.0,1.0]
		buttonArray = [1.0, 1.0, 1.0, 1.0]


		axesArray.insert(0,data.axes[0])
		axesArray.insert(1,data.axes[1])
		axesArray.insert(2,data.axes[3])
		axesArray.insert(3,data.axes[4])
		axesArray=axesArray[:-4]

		buttonArray.insert(0,data.buttons[11])
		buttonArray.insert(1,data.buttons[12])
		buttonArray.insert(2,data.buttons[13])
		buttonArray.insert(3,data.buttons[14])
		buttonArray=buttonArray[:-4]

		xdata = ET.Element('data')
		xitems = ET.SubElement(xdata, 'axes')
		xitem1 = ET.SubElement(xitems, 'item')
		xitem2 = ET.SubElement(xitems, 'item')
		xitem3 = ET.SubElement(xitems, 'item')
		xitem4 = ET.SubElement(xitems, 'item')
		xitem5 = ET.SubElement(xitems, 'item')
		xitem6 = ET.SubElement(xitems, 'item')
		xitem7 = ET.SubElement(xitems, 'item')
		xitem8 = ET.SubElement(xitems, 'item')
		xitem1.set('name','Left_X')
		xitem2.set('name','Left_Y')
		xitem3.set('name','Right_X')
		xitem4.set('name','Right_Y')
		xitem5.set('name','D_Left')
		xitem6.set('name','D_Right')
		xitem7.set('name','D_Up')
		xitem8.set('name','D_Down')
		xitem1.text = str(axesArray[0])
		xitem2.text = str(axesArray[1])
		xitem3.text = str(axesArray[2])
		xitem4.text = str(axesArray[3])
		xitem5.text = str(buttonArray[0])
		xitem6.text = str(buttonArray[1])
		xitem7.text = str(buttonArray[2])
		xitem8.text = str(buttonArray[3])

		mydata = ET.tostring(xdata)
		ser.write(mydata)
		ser.write('\n')

		print "AXES:"
		print axesArray
		print "BUTTONS:"
		print buttonArray

		temp = read_temp(tempOldSerialData)
		#print(temp)
		oled_temp(disp, temp)
		time.sleep(0.01)

	def readXbox():
		rospy.init_node('readXbox',anonymous=False)
		rospy.Subscriber("joy",Joy,callback)

		pubAxes = rospy.Publisher("axes",String,queue_size=10)

		rospy.spin()

	if __name__=='__main__':
		readXbox()

	def signal_handler(signal, frame):
		print('Exiting...')
		sys.exit(0)
	signal.signal(signal.SIGINT, signal_handler)

