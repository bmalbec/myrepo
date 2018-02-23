import xml.etree.ElementTree as ET
import serial
import time
import os

port = serial.Serial('/dev/ttyO4', 38400, timeout=0.1)

while True:
	time.sleep(.1)
	myfile = open('xboxAxes.xml','r')
#	myfile = open('xboxAxes.txt','r')
	myInfo = myfile.read()
	port.write(myInfo)
	statinfo = os.stat('xboxAxes.xml')
#	statinfo = os.stat('xboxAxes.txt')
	print statinfo.st_size

###############################################################################
#####	Testing if script can read values from the .xml file	###############
###############################################################################
#
#while True:
#	time.sleep(.1)
#	tree = ET.parse('xboxAxes.xml')
#	root = tree.getroot()
#	root = ET.fromstring(country_data_as_string)
#
#	for elem in root:
#		for subelem in elem:
#
#			print(subelem.text)
#
###############################################################################



	#data = ET.Element('data')
	#items = ET.SubElement(data, 'items')
	#item1 = ET.SubElement(items, 'item')
	#item2 = ET.SubElement(items, 'item')
	#item1.set('name','item1')
	#item2.set('name','item2')
	#item1.text = 'item1abc'
	#item2.text = 'item2abc'

	#mydata = ET.tostring(data)
	#myfile = open("items2.xml", "w")
	#myfile.write(mydata)
