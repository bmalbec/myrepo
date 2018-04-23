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

def init_pwm(i2c_address, pwm_freq):
	pwm = PWM(i2c_address) 		#create a pwm object for PCA9685 at i2c_address
	pwm.set_pwm_freq(pwm_freq) 	#set desired pwm freq

	return pwm

def init_temp():
	ADC.setup()
	time.sleep(0.001)

def init_pwm_values(pwm_xml_init_file):
	pwm_xml_init = open(pwm_xml_init_file, 'r')	#open initialization xml for pwm values
	time.sleep(0.001)
	pwm_init_values = pwm_xml_init.read()		#read the initial pwm values into pwmInitValues
	time.sleep(0.001)
	pwm_xml_init.close()						#close initialization xml
	time.sleep(0.001)

	return pwm_init_values

def init_temp_xml():
	temp_data = ET.Element('data')
	temp_item = ET.SubElement(temp_data, 'temp')
	temp_item_container = ET.SubElement(temp_item, 'item')
	temp_item_container.set('name','Temperature')
	temp_item_container.text = "0.0"

	return temp_data

def read_pwm_values(pwm_init_values, pwm_xml_current_file, ser):
	
#	Added April 11th by Brian Malbec to try and prevent crashes
	try:
		time.sleep(0.01)
		pwm_xml = open(pwm_xml_current_file, 'w+')	#open the xml for current pwm values
		time.sleep(0.001)
		pwm_current_values = ser.readline()					#read the incoming values
		time.sleep(0.001)

		if not pwm_current_values:							#if no incoming data
			pwm_current_values = pwm_init_values				#set the pwm values to initial values

		pwm_xml.write(pwm_current_values)
		time.sleep(0.001)
		pwm_xml.close()							#close the xml file
		time.sleep(0.001)

	except ET.ParseError:
		time.sleep(0.01)
		pwm_xml = open(pwm_xml_current_file, 'w+')
		time.sleep(0.01)
		pwm_xml.write(pwm_init_values)
		time.sleep(0.01)
		pwm_xml.close()
		time.sleep(0.01)
		
def parse_pwm_values(pwm_xml):
	try:
		time.sleep(0.009)
		pwm_tree = ET.parse(pwm_xml)	#parse the current values
		time.sleep(0.001)
		pwm_root = pwm_tree.getroot()				#get the root of the parse tree

		left_x = float(pwm_root[0][0].text)
		left_y = float(pwm_root[0][1].text)
		right_x = float(pwm_root[0][2].text)
		right_y = float(pwm_root[0][3].text)
		d_left = int(pwm_root[0][4].text)
		d_right = int(pwm_root[0][5].text)
		d_up = int(pwm_root[0][6].text)
		d_down = int(pwm_root[0][7].text)

		return (left_x, left_y, right_x, right_y, 
			d_left, d_right, d_up, d_down)
	
	except ET.ParseError:
		return (0, 0, 0, 0, 0, 0, 0, 0)
	
def calculate_motor_speeds(left_x, left_y, right_x, right_y, 
			   d_left, d_right, d_up, d_down, 
			   prev_value_LX, prev_value_LY, prev_value_RX, prev_value_RY):

#	Added April 11th by Brian Malbec to prevent crashes
	try:
		old_min = -1
		old_max = 1
		new_min = 2300
		new_max = 3700

		max_jump = 100

		ceiling = new_max
		floor = new_min

		#temp = new_min
		new_max = (new_max - new_min) / 2
		new_min = 0

		old_range = old_max - old_min
		new_range = new_max - new_min

		#stopped=temp+new_max		commented out bc "temp" is redundant of "floor", and it's only used here 
		stopped = floor + new_max
		threshold = new_max / 2

		new_value_LX = int(((left_x - old_min) * new_range) / old_range) + new_min
		new_value_LY = int(((left_y - old_min) * new_range) / old_range) + new_min
		new_value_RX = int(((right_x - old_min) * new_range) / old_range) + new_min
		new_value_RY = int(((right_y - old_min) * new_range) / old_range) + new_min

		motor1 = stopped
		motor2 = stopped
		motor3 = stopped
		motor4 = stopped
		motor5 = stopped
		motor6 = stopped

	#	if abs(newValueLX - prevValueLX) > threshold:
	#		newValueLX = ramp_formula(prevValueLX, newValueLX)
	#	if abs(newValueLY - prevValueLY) > threshold:
	#		newValueLY = ramp_formula(prevValueLY, newValueLY)
	#	if abs(newValueRX - prevValueRX) > threshold:
	#		newValueRX = ramp_formula(prevValueRX, newValueRX)
	#	if abs(newValueRY - prevValueRY) > threshold:
	#		newValueRY = ramp_formula(prevValueRY, newValueRY)

		if (new_value_LX - prev_value_LX) > max_jump:
			new_value_LX = prev_value_LX + max_jump
		else:
			if (prev_value_LX - new_value_LX) > max_jump:
				new_value_LX = prev_value_LX - max_jump

		if (new_value_LY - prev_value_LY) > max_jump:
			new_value_LY = prev_value_LY + max_jump
		else:
			if (prev_value_LY - new_value_LY) > max_jump:
				new_value_LY = prev_value_LY - max_jump

		if (new_value_RX - prev_value_RX) > max_jump:
			new_value_RX = prev_value_RX + max_jump
		else:
			if (prev_value_RX - new_value_RX) > max_jump:
				new_value_RX = prev_value_RX - max_jump		

		if (new_value_RY - prev_value_RY) > max_jump:
			new_value_RY = prev_value_RY + max_jump
		else:
			if (prev_value_RY - new_value_RY) > max_jump:
				new_value_RY = prev_value_RY - max_jump

		prev_value_LX = new_value_LX
		prev_value_LY = new_value_LY
		prev_value_RX = new_value_RX
		prev_value_RY = new_value_RY

	#	LEFT
		if new_value_LX > threshold:
			#print "\t\tLEFT"
			left_val = new_value_LX - threshold
			motor1 -= left_val
			motor2 += left_val
			motor3 += left_val
			motor4 -= left_val

	#	RIGHT
		if new_value_LX < threshold:
			#print "\t\tRIGHT"
			right_val = threshold - new_value_LX
			motor1 += right_val
			motor2 -= right_val
			motor3 -= right_val
			motor4 += right_val

	#	FORWARD
		if new_value_LY > threshold:
			#print "\t\tFORWARD"
			fwd_val = new_value_LY - threshold
			motor1 += fwd_val
			motor2 += fwd_val
			motor3 += fwd_val
			motor4 += fwd_val

	#	BACKWARD
		if new_value_LY < threshold:
			#print "\t\tBACKWARD"
			back_val = threshold - new_value_LY
			motor1 -= back_val
			motor2 -= back_val
			motor3 -= back_val
			motor4 -= back_val

	#	ROTATE LEFT
		if new_value_RX > threshold:
			#print "\t\tROTATE LEFT"
			rotate_left_val = new_value_RX - threshold
			motor1 -= rotate_left_val
			motor2 += rotate_left_val
			motor3 -= rotate_left_val
			motor4 += rotate_left_val

	#	ROTATE RIGHT
		if new_value_RX < threshold:
			#print "\t\tROTATE RIGHT"
			rotate_right_val = threshold - new_value_RX
			motor1 += rotate_right_val
			motor2 -= rotate_right_val
			motor3 += rotate_right_val
			motor4 -= rotate_right_val

	#	ASCEND
		if new_value_RY > threshold:
			#print "\t\tASCEND"
			ascend_val = 2 * (new_value_RY - threshold)
			motor5 -= ascend_val
			motor6 -= ascend_val

	#	DESCEND
		if new_value_RY < threshold:
			#print "\t\tDESCEND"
			descend_val = 2 * (threshold - new_value_RY)
			motor5 += descend_val
			motor6 += descend_val

	#	Restrict final motor values within the allowed bounds
		if motor1 > ceiling:
			motor1 = ceiling
		if motor1 < floor:
			motor1 = floor
		if motor2 > ceiling:
			motor2 = ceiling
		if motor2 < floor:
			motor2 = floor
		if motor3 > ceiling:
			motor3 = ceiling
		if motor3 < floor:
			motor3 = floor
		if motor4 > ceiling:
			motor4 = ceiling
		if motor4 < floor:
			motor4 = floor
		if motor5 > ceiling:
			motor5 = ceiling
		if motor5 < floor:
			motor5 = floor
		if motor6 > ceiling:
			motor6 = ceiling
		if motor6 < floor:
			motor6 = floor

		return (motor1, motor2, motor3, motor4, motor5, motor6, 
			prev_value_LX, prev_value_LY, prev_value_RX, prev_value_RY)

	except ET.ParseError:
		return (0,0,0,0,0,0,0,0,0,0)

def set_motor_speeds(pwm, motor1, motor2, motor3, motor4, motor5, motor6, 
		     d_left, d_right, d_up, d_down, 
		     servo_turn, servo_grip, servo_min, servo_max):

#	Added April 11th by Brian Malbec to prevent crashes
	try:
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

	#		Rotate Left
		if d_left == 1:
			servo_turn -=500
		else:
	#		Rotate Right	
			if d_right == 1:
				servo_turn +=500

	#		Open
		if d_up == 1:
			servo_grip -= 500
		else:
	#		Close
			if d_down == 1:
				servo_grip += 500


	##########	Added on March 23, 2018 by Brian Malbec because without it, 
	##########	code may not know "servo_min" and "servo_max" to be global variables
		#servo_max = 4000
		#servo_min = 1200
		#servo_max = 3900
		#servo_min = 1400
	##########################################################################

	#		Restrict servo values within the allowed bounds
		if servo_turn > servo_max:
			servo_turn = servo_max
		if servo_turn < servo_min:
			servo_turn = servo_min
		if servo_grip > servo_max:
			servo_grip = servo_max
		if servo_grip < servo_min:
			servo_grip = servo_min


		servo_turn_local = servo_turn
		servo_grip_local = servo_grip

	#		Set the PWM of each servo
		pwm.set_pwm(6,0,servo_grip_local)
		pwm.set_pwm(7,0,servo_turn_local)

		return servo_turn_local, servo_grip_local

	except ET.ParseError:
		return 2500, 2500

def new_temp_xml(raw_temp):

	temp_data = ET.Element('data')
	temp_item = ET.SubElement(temp_data, 'temp')
	temp_item_container = ET.SubElement(temp_item, 'item')
	temp_item_container.set('name','Temperature')
	temp_item_container.text = str(raw_temp)

	return temp_data

def send_temp(temp_pin, ser):

#	Added April 11th by Brian Malbec to prevent crashes
	try:
		raw_temp = ADC.read(temp_pin)
		time.sleep(0.001)
		millivolts = raw_temp * 1800	
		temp_C = float("{0:.1f}".format((millivolts - 803) / 8))
		temp_data = new_temp_xml(temp_C)
		temp_XML = ET.tostring(temp_data)
		ser.write(temp_XML)
		ser.write('\n')

	except ET.ParseError:
		pass
		
##############################################
############# Set Parameters #################
##############################################

temp_pin = "AIN1"

i2c_address = 0x40
pwm_freq = 485

pwm_xml_init_file = '/home/ubuntu/testfile5.xml'
pwm_xml_current_file = '/home/ubuntu/testfile4.xml'

ser = serial.Serial('/dev/ttyO4', 38400, timeout=0.15)

prev_value_LX = 3000
prev_value_LY = 3000
prev_value_RX = 3000
prev_value_RY = 3000

servo_turn = 2500
servo_grip = 2500
#servo_max = 4000
#servo_min = 1200
#	Added April 23rd by Brian, making a wider range for the servo to turn & grip
servo_max = 4500
servo_min = 0
#servo_max = 3900
#servo_min = 1400

###############################################
####### Call Initialization Functions #########
###############################################
pwm = init_pwm(i2c_address, pwm_freq)
init_temp()
temp_data = init_temp_xml()
pwm_init_values = init_pwm_values(pwm_xml_init_file)

##############################################
################### Main #####################
##############################################
while True:
	try:
		read_pwm_values(pwm_init_values, pwm_xml_current_file, ser)
		#lx, ly, rx, ry,
		left_x, left_y, right_x, right_y, d_left, d_right, d_up, d_down = parse_pwm_values(pwm_xml_current_file)

		motor1, motor2, motor3, motor4, motor5, motor6, prev_value_LX, prev_value_LY, prev_value_RX, prev_value_RY = calculate_motor_speeds(left_x, left_y, right_x, right_y, d_left, d_right, d_up, d_down, prev_value_LX, prev_value_LY, prev_value_RX, prev_value_RY)

		servo_turn, servo_grip = set_motor_speeds(pwm, motor1, motor2, motor3, motor4, motor5, motor6, d_left, d_right, d_up, d_down, servo_turn, servo_grip, servo_min, servo_max)

		send_temp(temp_pin, ser)
		
	except ET.ParseError:
		pass
