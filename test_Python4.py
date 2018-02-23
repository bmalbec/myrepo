import xml.etree.ElementTree as ET
import xml.dom.minidom
import serial
import time
import re
import sys
#from xml.etree import ElementTree

#	group 1 works together


#tree = ET.parse('testfile4.xml')			group 1
#root = tree.getroot()					group 1


old_min = -1
old_max = 1

#######################################################################################
#######################################################################################
########################	CHANGE THESE VALUES	###############################
#######################################################################################
										#######
new_min = 500									#######
new_max = 1000									#######
										#######
#######################################################################################
#######################################################################################
#######################################################################################
#######################################################################################





temp = new_min	
new_max = (new_max-new_min)/2
new_min = 0	

old_range = old_max - old_min
new_range = new_max - new_min


stopped=temp+new_max 
threshold= new_max/2

while True:
#	for elem in root:				group 1
#		for subelem in elem.findall('item'):	group 1
			#print(subelem.get('name'))	group 1
	time.sleep(1)
#	tree = ET.parse('testfile4.xml')
#	root = tree.getroot()
	root = ET.fromstring(open("testfile4.xml").read())

	lx = float(root[0][0].text)
	ly = float(root[0][1].text)
	rx = float(root[0][2].text)
	ry = float(root[0][3].text)

#	Original calculations
	
	newValueLX=int(((lx-old_min)*new_range)/old_range)+new_min
	newValueLY=int(((ly-old_min)*new_range)/old_range)+new_min
	newValueRX=int(((rx-old_min)*new_range)/old_range)+new_min
	newValueRY=int(((ry-old_min)*new_range)/old_range)+new_min

#	newValueLX=int((((lx-old_min)*new_range)/old_range)+new_min)/2
#	newValueLY=int((((ly-old_min)*new_range)/old_range)+new_min)/2
#	newValueRX=int((((rx-old_min)*new_range)/old_range)+new_min)/2
#	newValueRY=int((((ry-old_min)*new_range)/old_range)+new_min)/2

#	make a case for each direction

	motor1=stopped
	motor2=stopped
	motor3=stopped
	motor4=stopped
	motor5=stopped
	motor6=stopped

#	threshold = new_max/2

#	LEFT
	if newValueLX > threshold:
		leftval = newValueLX - threshold
		motor1 -= leftval
		motor2 += leftval
		motor3 += leftval
		motor4 -= leftval

#	RIGHT
	if newValueLX <= threshold:
		rightval = threshold - newValueLX
		motor1 += rightval
		motor2 -= rightval
		motor3 -= rightval
		motor4 += rightval

#	FORWARD
	if newValueLY > threshold:
		fwdval = newValueLY - threshold
		motor1 += fwdval
		motor2 += fwdval
		motor3 += fwdval
		motor4 += fwdval

#	BACKWARD
	if newValueLY <= threshold:
		backval = threshold - newValueLY
		motor1 -= backval
		motor2 -= backval
		motor3 -= backval
		motor4 -= backval

#	ROTATE LEFT
	if newValueRX > threshold:
		rotateleftval = newValueRX - threshold
		motor1 -= rotateleftval
		motor2 += rotateleftval
		motor3 -= rotateleftval
		motor4 += rotateleftval

#	ROTATE RIGHT
	if newValueRX <= threshold:
		rotaterightval = threshold - newValueRX
		motor1 += rotaterightval
		motor2 -= rotaterightval
		motor3 += rotaterightval
		motor4 -= rotaterightval

#	ASCEND 
	if newValueRY > threshold:
		ascendval = 2*(newValueRY - threshold)
		motor5 += ascendval
		motor6 += ascendval

#	DESCEND
	if newValueRY <= threshold:
		descendval = 2*(threshold - newValueRY)
		motor5 -= descendval
		motor6 -= descendval
	

	print "AXES:"
	print "LX: %i" % newValueLX
	print "LY: %i" % newValueLY
	print "RX: %i" % newValueRX
	print "RY: %i" % newValueRY

#	motor1=	+800
#	motor2=	+800
#	motor3=	+800
#	motor4=	+800
#	motor5=	+800
#	motor6=	+800
	
	print "MOTORS:"
	print "1: %i" % motor1
	print "2: %i" % motor2
	print "3: %i" % motor3
	print "4: %i" % motor4
	print "5: %i" % motor5
	print "6: %i" % motor6
#	topleft = 

#	for elem in root:
#		for subelem in elem:
#			print(root[0][2].text)

