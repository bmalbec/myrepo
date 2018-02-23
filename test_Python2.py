import xml.etree.ElementTree as ET
import xml.dom.minidom
import serial
import time
import re
from shutil import copyfile

ser = serial.Serial('/dev/ttyUSB0', 38400, timeout=0.1)
#ser.flushInput()
#ser.flushOutput()
count = 0


#mybackup = open("testfile5.xml",'r')
#backup = mybackup.read()
#mybackup2 = open("testfile6.xml",'w')
#cover = mybackup2.write(backup)
#mybackup.close()
#mybackup2.close()

#print backup
#print "ass"

while True:


	myfile = open("testfile4.xml",'w')
#Just showing that packets are constantly coming in, even if the joystick isn't being pressed 
	count+=1
	print "PACKET # %i" % count
#############################################################################################
	

####	practice stuff	#####

#	tree = ET.parse("testfile4.xml")
#	root = tree.getroot()
###############################








	mydata = ser.readline()
#	mydata = str(ser.readline())

#	if mydata:
#		mybackup=open('testfile6.xml','w')
#		mybackup.write(mydata)
#		mybackup.close()
#	if not mydata:
#		mydatas = open('testfile6.xml','r')
#		mydata = mydatas.read()
#		mydatas.close()

#		backup = mydata
	#mydata.close()
#	root = ET.fromstring(mydata)

	
	myfile.write(mydata)

#	copyfile("testfile4.xml","testfile5.xml")

#	tree = ET.parse('testfile5.xml')
#	root = tree.getroot()

#	print "derp"
	print mydata
	

###		NEW DATA	###
	
#	myfile.close()
	
#	tree = ET.parse('testfile4.xml')
#	root = tree.getroot()

#	print(float(root[0][0].text))	









#	myfile = open("testfile4.xml",'r')
#	tree = ET.parse('testfile4.xml')
#	tree = ET.parse('testfile4.xml').getroot()
#	root = tree.getroot()
#	root = ET.Element('data')
#	head = ET.SubElement(root, 'axes')
#	item1 = ET.SubElement(head, 'item')
#	item2 = ET.SubElement(head, 'item')
#	item3 = ET.SubElement(head, 'item')
#	item4 = ET.SubElement(head, 'item')
#	item1.set('name','Left_X')
#	item2.set('name','Left_Y')
#	item3.set('name','Right_X')
#	item4.set('name','Right_Y')
#	item1.text = root[0][0].text
#	item2.text = root[0][1].text
#	item3.text = root[0][2].text
#	finaldata = ET.tostring(root)
#	print(item1.text)

