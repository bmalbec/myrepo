import xml.etree.ElementTree as ET
import xml.dom.minidom
import serial
import time
import re
import Adafruit_BBIO.ADC as ADC
import struct
import math
from shutil import copyfile
from Adafruit_PCA9685 import PCA9685 as PWM

###########################################
########### Declare Functions #############
###########################################

def init_pwm(i2cAddress, pwmFreq):
	pwm = PWM(i2cAddress) 		#create a pwm object for PCA9685 at i2cAddress
	pwm.set_pwm_freq(pwmFreq) 	#set desired pwm freq

	return pwm

def init_temp():
	ADC.setup()
	time.sleep(0.001)

def init_pwm_values(pwmXmlInitFile):
	pwmXmlInit = open(pwmXmlInitFile, 'r')	#open initialization xml for pwm values
	time.sleep(0.001)
	pwmInitValues = pwmXmlInit.read()		#read the initial pwm values into pwmInitValues
	time.sleep(0.001)
	pwmXmlInit.close()						#close initialization xml
	time.sleep(0.001)

	return pwmInitValues

def init_temp_xml():
	tempData = ET.Element('data')
	tempItem = ET.SubElement(tempData, 'temp')
	tempItem1 = ET.SubElement(tempItem, 'item')
	tempItem1.set('name','Temperature')
	tempItem1.text = "0.0"

	return tempData

def read_pwm_values(pwmInitValues, pwmXmlCurrentFile, ser):
	time.sleep(0.01)
	pwmXmlCurrentValues = open(pwmXmlCurrentFile, 'w+')	#open the xml for current pwm values
	time.sleep(0.001)
	pwmCurrentValues = ser.readline()					#read the incoming values
	time.sleep(0.001)

	if not pwmCurrentValues:							#if no incoming data
		pwmCurrentValues = pwmInitValues				#set the pwm values to initial values

	pwmXmlCurrentValues.write(pwmCurrentValues)
	time.sleep(0.001)
	pwmXmlCurrentValues.close()							#close the xml file
	time.sleep(0.001)

def parse_pwm_values(pwmXmlCurrentFile):
	try:
		time.sleep(0.009)
		pwmTree = ET.parse(pwmXmlCurrentFile)	#parse the current values
		time.sleep(0.001)
		pwmRoot = pwmTree.getroot()				#get the root of the parse tree

		lx = float(pwmRoot[0][0].text)
		ly = float(pwmRoot[0][1].text)
		rx = float(pwmRoot[0][2].text)
		ry = float(pwmRoot[0][3].text)
		d_left = int(pwmRoot[0][4].text)
		d_right = int(pwmRoot[0][5].text)
		d_up = int(pwmRoot[0][6].text)
		d_down = int(pwmRoot[0][7].text)

		return lx, ly, rx, ry, d_left, d_right, d_up, d_down
	
	except ET.ParseError:
		return 0, 0, 0, 0, 0, 0, 0, 0

#def ramp_formula(oldValue, currentValue):	
#	difference =
	
def calculate_motor_speeds(lx, ly, rx, ry, d_left, d_right, d_up, d_down, prevValueLX, prevValueLY, prevValueRX, prevValueRY):
	old_min = -1
	old_max = 1
	new_min = 2300
	new_max = 3700
	
	max_jump = 100
	
	ceiling = new_max
	floor = new_min

	temp = new_min
	new_max = (new_max-new_min)/2
	new_min = 0

	old_range = old_max - old_min
	new_range = new_max - new_min

	stopped=temp+new_max
	threshold= new_max/2

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

#	if abs(newValueLX - prevValueLX) > threshold:
#		newValueLX = ramp_formula(prevValueLX, newValueLX)
#	if abs(newValueLY - prevValueLY) > threshold:
#		newValueLY = ramp_formula(prevValueLY, newValueLY)
#	if abs(newValueRX - prevValueRX) > threshold:
#		newValueRX = ramp_formula(prevValueRX, newValueRX)
#	if abs(newValueRY - prevValueRY) > threshold:
#		newValueRY = ramp_formula(prevValueRY, newValueRY)

	if (newValueLX - prevValueLX) > max_jump:
		newValueLX = prevValueLX + max_jump
	else:
		if (prevValueLX - newValueLX) > max_jump:
			newValueLX = prevValueLX - max_jump
		
	if (newValueLY - prevValueLY) > max_jump:
		newValueLY = prevValueLY + max_jump
	else:
		if (prevValueLY - newValueLY) > max_jump:
			newValueLY = prevValueLY - max_jump
		
	if (newValueRX - prevValueRX) > max_jump:
		newValueRX = prevValueRX + max_jump
	else:
		if (prevValueRX - newValueRX) > max_jump:
			newValueRX = prevValueRX - max_jump		

	if (newValueRY - prevValueRY) > max_jump:
		newValueRY = prevValueRY + max_jump
	else:
		if (prevValueRY - newValueRY) > max_jump:
			newValueRY = prevValueRY - max_jump
		
	prevValueLX = newValueLX
	prevValueLY = newValueLY
	prevValueRX = newValueRX
	prevValueRY = newValueRY
	
#	LEFT
	if newValueLX > threshold:
		#print "\t\tLEFT"
		leftval = newValueLX - threshold
		motor1 -= leftval
		motor2 += leftval
		motor3 += leftval
		motor4 -= leftval
#	RIGHT
	if newValueLX < threshold:
		#print "\t\tRIGHT"
		rightval = threshold - newValueLX
		motor1 += rightval
		motor2 -= rightval
		motor3 -= rightval
		motor4 += rightval
#	FORWARD
	if newValueLY > threshold:
		#print "\t\tFORWARD"
		fwdval = newValueLY - threshold
		motor1 += fwdval
		motor2 += fwdval
		motor3 += fwdval
		motor4 += fwdval
#	BACKWARD
	if newValueLY < threshold:
		#print "\t\tBACKWARD"
		backval = threshold - newValueLY
		motor1 -= backval
		motor2 -= backval
		motor3 -= backval
		motor4 -= backval
#	ROTATE LEFT
	if newValueRX > threshold:
		#print "\t\tROTATE LEFT"
		rotateleftval = newValueRX - threshold
		motor1 -= rotateleftval
		motor2 += rotateleftval
		motor3 -= rotateleftval
		motor4 += rotateleftval

#	ROTATE RIGHT
	if newValueRX < threshold:
		#print "\t\tROTATE RIGHT"
		rotaterightval = threshold - newValueRX
		motor1 += rotaterightval
		motor2 -= rotaterightval
		motor3 += rotaterightval
		motor4 -= rotaterightval
#	ASCEND
	if newValueRY > threshold:
		#print "\t\tASCEND"
		ascendval = 2*(newValueRY - threshold)
		motor5 -= ascendval
		motor6 -= ascendval
#	DESCEND
	if newValueRY < threshold:
		#print "\t\tDESCEND"
		descendval = 2*(threshold - newValueRY)
		motor5 += descendval
		motor6 += descendval

	if motor1>ceiling:
		motor1=ceiling
	if motor1<floor:
		motor1=floor
	if motor2>ceiling:
		motor2=ceiling
	if motor2<floor:
		motor2=floor
	if motor3>ceiling:
		motor3=ceiling
	if motor3<floor:
		motor3=floor
	if motor4>ceiling:
		motor4=ceiling
	if motor4<floor:
		motor4=floor
	if motor5>ceiling:
		motor5=ceiling
	if motor5<floor:
		motor5=floor
	if motor6>ceiling:
		motor6=ceiling
	if motor6<floor:
		motor6=floor

	return motor1, motor2, motor3, motor4, motor5, motor6, prevValueLX, prevValueLY, prevValueRX, prevValueRY

def set_motor_speeds(pwm, motor1, motor2, motor3, motor4, motor5, motor6, d_left, d_right, d_up, d_down, servoTurn, servoGrip):
	#time.sleep(0.1)
	pwm.set_pwm(0,0,motor1)
	#time.sleep(0.1)
	pwm.set_pwm(5,0,motor2)
	#time.sleep(0.1)
	pwm.set_pwm(2,0,motor3)
	#time.sleep(0.1)
	pwm.set_pwm(3,0,motor4)
	#time.sleep(0.1)
	pwm.set_pwm(4,0,motor5)
	#time.sleep(0.1)
	pwm.set_pwm(1,0,motor6)
	#time.sleep(0.1)
	
#	if d_left == 1:
		#	turn left
#	else:
#		if d_right == 1:
			#	turn right
	
	if d_up == 1:
		#	open
	else:
		if d_down == 1:
			#	close
	
	return servoTurn, servoGrip

def new_temp_xml(rawTemp):
	tempData = ET.Element('data')
	tempItem = ET.SubElement(tempData, 'temp')
	tempItem1 = ET.SubElement(tempItem, 'item')
	tempItem1.set('name','Temperature')
	tempItem1.text = str(rawTemp)

	return tempData

def send_temp(tempPin, ser):
	#rawTemp = round(ADC.read(tempPin),1)
	rawTemp = ADC.read(tempPin)
	time.sleep(0.001)
	millivolts = rawTemp * 1800
	#tempC = (millivolts - 800) / 10
	tempC = float("{0:.1f}".format((millivolts - 803) / 8))
	tempData = new_temp_xml(tempC)
	tempXML = ET.tostring(tempData)
	ser.write(tempXML)
	ser.write('\n')
	#print(rawTemp)
	#print tempC
	
##############################################
############# Set Parameters #################
##############################################

tempPin = "AIN1"

i2cAddress = 0x40
pwmFreq = 485

pwmXmlInitFile = '/home/ubuntu/testfile5.xml'
pwmXmlCurrentFile = '/home/ubuntu/testfile4.xml'

ser = serial.Serial('/dev/ttyO4', 38400, timeout=0.15)

prevValueLX = 3000
prevValueLY = 3000
prevValueRX = 3000
prevValueRY = 3000

servoTurn = 2600
servoGrip = 2600


###############################################
####### Call Initialization Functions #########
###############################################

pwm = init_pwm(i2cAddress, pwmFreq)
init_temp()
tempData = init_temp_xml()
pwmInitValues = init_pwm_values(pwmXmlInitFile)

##############################################
################### Main #####################
##############################################

while True:
	try:
		read_pwm_values(pwmInitValues, pwmXmlCurrentFile, ser)

		lx, ly, rx, ry, d_left, d_right, d_up, d_down = parse_pwm_values(pwmXmlCurrentFile)

		motor1, motor2, motor3, motor4, motor5, motor6, prevValueLX, prevValueLY, prevValueRX, prevValueRY = calculate_motor_speeds(lx, ly, rx, ry, d_left, d_right, d_up, d_down, prevValueLX, prevValueLY, prevValueRX, prevValueRY)

		servoTurn, servoGrip = set_motor_speeds(pwm, motor1, motor2, motor3, motor4, motor5, motor6, d_left, d_right, d_up, d_down, servoTurn, servoGrip)

		send_temp(tempPin, ser)
		x=4000
		i=1200
		
		while i < x:
			pwm.set_pwm(0,0,i)
			print "rise %i" % i
			i+=10
		
		x=4000
		i=1200
		
		while x > i:
			pwm.set_pwm(0,0,x)
			print "fall %i" % x
	
			x-=10
						
		#print "AXES:"
		#print "LX: %i" % newValueLX
		#print "LY: %i" % newValueLY
		#print "RX: %i" % newValueRX
		#print "RY: %i" % newValueRY

		#print "MOTORS:"
		#print "1: %i" % motor1
		#print "2: %i" % motor2
		#print "3: %i" % motor3
		#print "4: %i" % motor4
		#print "5: %i" % motor5
		#print "6: %i" % motor6

		#print "BUTTONS:"
		#print "D-Pad Left: %i" % d_left
		#print "D-Pad Right: %i" % d_right
		#print "D-Pad Up: %i" % d_up
		#print "D-Pad Down: %i" % d_down
		#print '\n'

	except ET.ParseError:
		pass
