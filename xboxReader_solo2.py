#!/usr/bin/env python

import rospy
import sys
import serial
import struct
import xml.etree.ElementTree as ET
import math
import signal

#from xmodem import XMODEM
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from std_msgs.msg import String, Char, Float64
#from Axes.msg import axes

#axesArray = []
axesArray = [1.0,1.0,1.0,1.0]
count=4

ser = serial.Serial('/dev/ttyO4', 38400)
while True:
	try:
		def callback(data):

		#ser = serial.Serial('/dev/ttyO4', 38400)
	#	ser.flush()
	#	ser.flushInput()
	#	ser.flushOutput()

#		item="[Left analog x: %.3f]" % data.axes[0]
#		item2="[Left analog y: %.3f]" % data.axes[1]
#		item3="[Right analog x: %.3f]" % data.axes[3]
#		item4="[Right analog y: %.3f]" % data.axes[4]
#		total=item+item2+item3+item4
		#axes.insert(data.axes[0],data.axes[1])#,data.axes[3],data.axes[4])
		#axes.append(data.axes[3])
		#axes.append(data.axes[4])
		#axes=[data.axes[0],data.axes[1],data.axes[3],data.axes[4]]

		#axesArray[1]=data.axes[0]
		#axesArray[2]=data.axes[1]
		#axesArray[3]=data.axes[3]
		#axesArray[4]=data.axes[4]
			axesArray = [1.0,1.0,1.0,1.0]

####	Method 1 (which works totally fine)	###########################

			axesArray.insert(0,data.axes[0])
			axesArray.insert(1,data.axes[1])
			axesArray.insert(2,data.axes[3])
			axesArray.insert(3,data.axes[4])
			axesArray=axesArray[:-4]
#################################################



####	Method 2	###########################
#	bumplx = float(data.axes[0])+1
#	bumply = float(data.axes[1])+1
#	bumprx = float(data.axes[3])+1
#	bumpry = float(data.axes[4])+1
#	lx = "%.5f" % bumplx
#	ly = "%.5f" % bumply
#	rx = "%.5f" % bumprx
#	ry = "%.5f" % bumpry
#	axesArray.insert(0,lx)
#	axesArray.insert(1,ly)
#	axesArray.insert(2,rx)
#	axesArray.insert(3,ry)
#	axesArray=axesArray[:-4]
###	testing with .txt files		###
#	myfile = open("xboxAxes.txt","w")
#	myfile.write(axesArray)
#	print axesArray

#################################################

#	sys.stdout.write("\r"+total)
	#for i in range(count):
	#test=ser.write(str(axesArray))
#	test=ser.write('\n')
#	sys.stdout.flush()
	#print axesArray


	# create the file structure
####	temporarily blocked out so i can test .txt files	####
			xdata = ET.Element('data')
			xitems = ET.SubElement(xdata, 'axes')
			xitem1 = ET.SubElement(xitems, 'item')
			xitem2 = ET.SubElement(xitems, 'item')
			xitem3 = ET.SubElement(xitems, 'item')
			xitem4 = ET.SubElement(xitems, 'item')
			xitem1.set('name','Left_X')
			xitem2.set('name','Left_Y')
			xitem3.set('name','Right_X')
			xitem4.set('name','Right_Y')
			xitem1.text = str(axesArray[0])
			xitem2.text = str(axesArray[1])
			xitem3.text = str(axesArray[2])
			xitem4.text = str(axesArray[3])



	# create a new XML file with the results
			mydata = ET.tostring(xdata)
			ser.write(mydata)
			ser.write('\n')
#	def getc(size, timeout=0.1):
#		return ser.read(size)
#	def putc(xdata, timeout=0.1):
#		ser.write(xdata)
#	modem = XMODEM(getc, putc)

#################	this stuff works temporarily	##############
	#	myfile = open("xboxAxes.xml", "w")
#	myfile = open('xboxAxes.xml','rb')
#	modem.send(myfile)
	#	myfile.write(mydata)
#	myfile.write('\n')
######################################################################
	#	ser.write(myfile)
		#ser.write(mydata)
		#ser.write('\n')
#		myfile.close()


#	print test
			print axesArray





		def readXbox():
			rospy.init_node('readXbox',anonymous=False)
			rospy.Subscriber("joy",Joy,callback)

			pubAxes = rospy.Publisher("axes",String,queue_size=10)

	#ser = serial.Serial('/dev/ttyUSB0', 38400)
	#test=ser.write('test')
	#print test
	#pubAxes.publish(axesArray)
	#pubAxes.publish(test)
	#ser.write("test")
			rospy.spin()

		if __name__=='__main__':
			readXbox()

		def signal_handler(signal, frame):
			print('Exiting...')
			sys.exit(0)
		signal.signal(signal.SIGINT, signal_handler)

	except KeyboardInterrupt:
		sys.exit()
