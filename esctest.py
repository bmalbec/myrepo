#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
import time

# Initialise the PWM device using the default address
pwm = PWM(0x40, debug=True)

servoMin = 0  # Min pulse length out of 4096
servoMax = 4096  # Max pulse length out of 4096

pwm.setPWMFreq(1000)                        # Set frequency to 60 Hz

while (True):
# Move servo back and forward on channel 0
	#pwm.setPWM(0, 0, servoMin)
	#time.sleep(2)
	#pwm.setPWM(0, 0, servoMax)
	#time.sleep(2)
	for i in range (400, 1100):
		pwm.setPWM(0,0,i)
		pwm.setPWM(1,1,i)
		time.sleep(0.05)
		print(i)
