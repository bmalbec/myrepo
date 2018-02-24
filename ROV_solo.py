import xml.etree.ElementTree as ET
import xml.dom.minidom
import serial
import time
import re
from shutil import copyfile
#from Adafruit_PCA9685 import PCA9685 as PWM

#default address
#pwm = PWM(0x40)

#set freq to 1000Hz
#pwm.set_pwm_freq(1000)

ser = serial.Serial('/dev/ttyUSB0', 38400, timeout=0.15)
time.sleep(5)
#ser.flushInput() ser.flushOutput()
count = 0
####	backup .xml files	############
mybackup = open("testfile5.xml",'r')
backup = mybackup.read()
mybackup2 = open("testfile6.xml",'w')
cover = mybackup2.write(backup)
mybackup.close()
mybackup2.close()
#############################################
old_min = -1
old_max = 1
new_min = 500
new_max = 1000

temp = new_min
new_max = (new_max-new_min)/2
new_min = 0

old_range = old_max - old_min
new_range = new_max - new_min

stopped=temp+new_max

threshold= new_max/2
while True:
	try:
		time.sleep(0.01)

	#Just showing that packets are constantly coming in, even if the
	#joystick isn't being pressed

	#	count+=1 print "PACKET # %i" % count
	########################	RECEIVING DATA ########################

		myfile = open("testfile4.xml",'w')
		mydata = ser.readline()
		if mydata:
			mybackup=open('testfile6.xml','w')
			mybackup.write(mydata)
			mybackup.close()
		if not mydata:
			mydatas = open('testfile6.xml','r')
			mydata = mydatas.read()
			mydatas.close()

		myfile.write(mydata)
	#	print mydata

	################################################################################
	###		PARSING DATA
	###		################################################

		myfile.close()
		time.sleep(0.001)
		tree = ET.parse('testfile4.xml')
		root = tree.getroot()
	#	print(float(root[0][0].text))
	################################################################################
	###########	MOTOR CALCULATIONS
	###########	########################################
		lx = float(root[0][0].text)
		ly = float(root[0][1].text)
		rx = float(root[0][2].text)
		ry = float(root[0][3].text)
		newValueLX=int(((lx-old_min)*new_range)/old_range)+new_min
		newValueLY=int(((ly-old_min)*new_range)/old_range)+new_min
		newValueRX=int(((rx-old_min)*new_range)/old_range)+new_min
		newValueRY=int(((ry-old_min)*new_range)/old_range)+new_min
		motor1=stopped
		motor2=stopped
		motor3=stopped
		motor4=stopped
		motor5=stopped
		motor6=stopped

		comparison = threshold/2
		compare_range = threshold - comparison
		print "\t\tTHRESHOLD %i" % compare_range

		if newValueLX == threshold and newValueLY == threshold and newValueRX == threshold and newValueRY == threshold:
			print "\t\tSTOPPED"
		else: 
		#	LEFT
#			if newValueLX > threshold and newValueLY > threshold-compare_range and newValueLY < threshold+compare_range:
			if newValueLX > threshold: 
#				if newValueLX > newValueLY:
#					print "\t\tLEFT"
#					leftval = newValueLX - threshold
#					motor1 -= leftval
#					motor2 += leftval
#					motor3 += leftval
#					motor4 -= leftval
				print "\t\tLEFT"
				leftval = newValueLX - threshold
				motor1 -= leftval
				motor2 += leftval
				motor3 += leftval
				motor4 -= leftval
		#	RIGHT
#			if newValueLX < threshold and newValueLY > threshold-compare_range and newValueLY < threshold+compare_range:
			if newValueLX < threshold:
#				if newValueLX < newValueLY:
#					print "\t\tRIGHT"
#					rightval = threshold - newValueLX
#					motor1 += rightval
#					motor2 -= rightval
#					motor3 -= rightval
#					motor4 += rightval
				print "\t\tRIGHT"
				rightval = threshold - newValueLX
				motor1 += rightval
				motor2 -= rightval
				motor3 -= rightval
				motor4 += rightval
		#	FORWARD
#			if newValueLY > threshold and newValueLX > threshold-compare_range and newValueLX < threshold+compare_range:
			if newValueLY > threshold:
#				if newValueLY > newValueLX:
#					print "\t\tFORWARD"
#					fwdval = newValueLY - threshold
#					motor1 += fwdval
#					motor2 += fwdval
#					motor3 += fwdval
#					motor4 += fwdval
				print "\t\tFORWARD"
				fwdval = newValueLY - threshold
				motor1 += fwdval
				motor2 += fwdval
				motor3 += fwdval
				motor4 += fwdval
		#	BACKWARD
#			if newValueLY < threshold and newValueLX > threshold-compare_range and newValueLX < threshold+compare_range:
			if newValueLY < threshold:
#				if newValueLY < newValueLX:
#					print "\t\tBACKWARD"
#					backval = threshold - newValueLY
#					motor1 -= backval
#					motor2 -= backval
#					motor3 -= backval
#					motor4 -= backval
				print "\t\tBACKWARD"
				backval = threshold - newValueLY
				motor1 -= backval
				motor2 -= backval
				motor3 -= backval
				motor4 -= backval
		#	ROTATE LEFT
#3			if newValueRX > threshold and newValueRY > threshold-compare_range and newValueRY < threshold+compare_range:
			if newValueRX > threshold:
#				if newValueRX > newValueRY:
#					print "\t\tROTATE LEFT"
#					rotateleftval = newValueRX - threshold
#					motor1 -= rotateleftval
#					motor2 += rotateleftval
#					motor3 -= rotateleftval
#					motor4 += rotateleftval
				print "\t\tROTATE LEFT"
				rotateleftval = newValueRX - threshold
				motor1 -= rotateleftval
				motor2 += rotateleftval
				motor3 -= rotateleftval
				motor4 += rotateleftval

		#	ROTATE RIGHT
#			if newValueRX < threshold and newValueRY > threshold-compare_range and newValueRY < threshold+compare_range:
			if newValueRX < threshold:
#				if newValueRX < newValueRY:
#					print "\t\tROTATE RIGHT"
#					rotaterightval = threshold - newValueRX
#					motor1 += rotaterightval
#					motor2 -= rotaterightval
#					motor3 += rotaterightval
#					motor4 -= rotaterightval
				print "\t\tROTATE RIGHT"
				rotaterightval = threshold - newValueRX
				motor1 += rotaterightval
				motor2 -= rotaterightval
				motor3 += rotaterightval
				motor4 -= rotaterightval
		#	ASCEND
			if newValueRY > threshold:
				print "\t\tASCEND"
				ascendval = 2*(newValueRY - threshold)
				motor5 += ascendval
				motor6 += ascendval
		#	DESCEND
			if newValueRY < threshold:
				print "\t\tDESCEND"
				descendval = 2*(threshold - newValueRY)
				motor5 -= descendval
				motor6 -= descendval

		if motor1>1000:
			motor1=1000
		if motor1<500:
			motor1=500
		if motor1>1000:
			motor1=1000
		if motor2<500:
			motor2=500
		if motor3>1000:
			motor3=1000
		if motor3<500:
			motor3=500
		if motor4>1000:
			motor4=1000
		if motor4<500:
			motor4=500
		if motor5>1000:
			motor5=1000
		if motor5<500:
			motor5=500
		if motor6>1000:
			motor6=1000
		if motor6<500:
			motor6=500


#		pwm.set_pwm(0,0,motor1)

		print "AXES:"
		print "LX: %i" % newValueLX
		print "LY: %i" % newValueLY
		print "RX: %i" % newValueRX
		print "RY: %i" % newValueRY
	#	motor1=	+800 motor2=	+800 motor3=	+800 motor4=	+800
	#	motor5=	+800 motor6=	+800

		print "MOTORS:"
		print "1: %i" % motor1
		print "2: %i" % motor2
		print "3: %i" % motor3
		print "4: %i" % motor4
		print "5: %i" % motor5
		print "6: %i" % motor6

		print '\n'
	###############################################################################
	except ET.ParseError:
		print "I crashed, oops"
#		pwm.set_pwm(0,0,motor1)
#		pwm.set_pwm(0,0,motor2)
#		pwm.set_pwm(0,0,motor3)
#		pwm.set_pwm(0,0,motor4)
#		pwm.set_pwm(0,0,motor5)
#		pwm.set_pwm(0,0,motor6)
