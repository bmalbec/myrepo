import time

import Adafruit_BBIO.GPIO as GPIO

#Constants
I2C_ADDRESS = 0x3C
CLEAR_DISPLAY = 0x01
RETURN_HOME = 0x20
ENTRY_MODE_SET_CURSOR_RIGHT_NOSHIFT = 0x07
ENTRY_MODE_SET_CURSOR_RIGHT_SHIFT = 0x06
ENTRY_MODE_SET_CURSOR_LEFT_NOSHIFT = 0x04
ENTRY_MODE_SET_CURSOR_LEFT_SHIFT = 0x05

#ROM_A Ref
def ROM_A_Switch(argument):
	ROM_A_Switcher = {
		" ":0x0F,
		"!":0x21,
		"#":0x23,
		"%":0x25,
		"&":0x26,
		"(":0x28,
		")":0x29,
		"*":0x2A,
		"+":0x2B,
		",":0x2C,
		"-":0x2D,
		".":0x2E,
		"/":0x2F,
		"0":0x30,
		"1":0x31,
		"2":0x32,
		"3":0x33,
		"4":0x34,
		"5":0x35,
		"6":0x36,
		"7":0x37,
		"8":0x38,
		"9":0x39,
		":":0x3A,
		";":0x3B,
		"<":0x3C,
		"=":0x3D,
		">":0x3E,
		"?":0x3F,
		"|":0x40,
		"A":0x41,
		"B":0x42,
		"C":0x43,
		"D":0x44,
		"E":0x45,
		"F":0x46,
		"G":0x47,
		"H":0x48,
		"I":0x49,
		"J":0x4A,
		"K":0x4B,
		"L":0x4C,
		"M":0x4D,
		"N":0x4E,
		"O":0x4F,
		"P":0x50,
		"Q":0x51,
		"R":0x52,
		"S":0x53,
		"T":0x54,
		"U":0x55,
		"V":0x56,
		"W":0x57,
		"X":0x58,
		"Y":0x59,
		"Z":0x5A,
		"a":0x61,
		"b":0x62,
		"c":0x63,
		"d":0x64,
		"e":0x65,
		"f":0x66,
		"g":0x67,
		"h":0x68,
		"i":0x69,
		"j":0x6A,
		"k":0x6B,
		"l":0x6C,
		"m":0x6D,
		"n":0x6E,
		"o":0x6F,
		"p":0x70,
		"q":0x71,
		"r":0x72,
		"s":0x73,
		"t":0x74,
		"u":0x75,
		"v":0x76,
		"w":0x77,
		"x":0x78,
		"y":0x79,
		"z":0x7A,
		"~":0x80,
		"[":0xFA,
		"]":0xFC,
		"$":0x82
	}
	return ROM_A_Switcher.get(argument)

def parse_string(string):
    parse = list(string)
    return parse

class US2066Base(object):
	"Base class for US2066 based OLED"

	def __init__(self, rst="P2_3", gpio=GPIO, i2c_bus=None, i2c_address=I2C_ADDRESS, i2c=None):
		self._i2c = None
		self._gpio = gpio
		if self._gpio is None:
			self._gpio = GPIO.get_platform_gpio()
		self._rst = rst
		if i2c is not None:
			self._i2c = i2c.get_i2c_device(i2c_address)
		else:
			import Adafruit_GPIO.I2C as I2C
			if i2c_bus is None:
				self._i2c = I2C.get_i2c_device(i2c_address)
			else:
				self._i2c = I2C.get_i2c_device(i2c_address, busnum=i2c_bus)

	def command(self, c):
		"Send command byte to display"
		control = 0x00
		self._i2c.write8(control, c)

	def data(self, c):
		"Send byte of data to display"
		control = 0x40
		self._i2c.write8(control, c)

	def begin(self):
		self.reset()
		self._initialize()
		self.command(0x0F) #turn on display

	def reset(self):
		"Reset the display"
		rst="P2_3"
		self._gpio.setup(rst, GPIO.OUT)
		self._gpio.output(rst, GPIO.HIGH)
		time.sleep(0.001)
		self._gpio.output(rst, GPIO.LOW)
		time.sleep(0.010)
		self._gpio.output(rst, GPIO.HIGH)

	def _initialize(self):
		self.command(0x2A)  #function set (extended self.command set)
		self.command(0x71)  #function selection A, disable internal Vdd regualtor
		self.data(0x00)
		self.command(0x28)  #function set (fundamental self.command set)
		self.command(0x08)  #display off, cursor off, blink off
		self.command(0x2A)  #function set (extended self.command set)
		self.command(0x79)  #OLED self.command set enabled
		self.command(0xD5)  #set display clock divide ratio/oscillator frequency
		self.command(0x70)  #set display clock divide ratio/oscillator frequency
		self.command(0x78)  #OLED self.command set disabled
		self.command(0x09)  #extended function set (4-lines)
		self.command(0x06)  #COM SEG direction
		self.command(0x72)  #function selection B, disable internal Vdd regualtor
		self.data(0x00)     #ROM CGRAM selection
		### my stuff	###
		self.command(0x40)
		self.data(0x1F)
		self.data(0x10)
		self.data(0x17)
		self.data(0x17)
		self.data(0x16)
		self.data(0x16)
		self.data(0x16)
		self.data(0x16)
		####################
		self.command(0x2A)  #function set (extended self.command set)
		self.command(0x79)  #OLED self.command set enabled
		self.command(0xDA)  #set SEG pins hardware configuration
		self.command(0x10)  #set SEG pins ... NOTE: When using NHD-0216AW-XB3 or NHD_0216MW_XB3 change to (0x00)
		self.command(0xDC)  #function selection C
		self.command(0x00)  #function selection C
		self.command(0x81)  #set contrast control
		self.command(0x7F)  #set contrast control
		self.command(0xD9)  #set phase length
		self.command(0xF1)  #set phase length
		self.command(0xDB)  #set VCOMH deselect level
		self.command(0x40)  #set VCOMH deselect level
		self.command(0x78)  #OLED self.command set disabled
		self.command(0x28)  #function set (fundamental self.command set)
		self.command(0x01)  #clear display
		self.command(0x80)  #set DDRAM address to 0x00
		time.sleep(.1)
	
	def write(self, argument):
    		parsed_string = parse_string(argument)
    		for i in range (0, len(parsed_string)):
        		data = ROM_A_Switch(parsed_string[i])
			if i == 20:
				self.command(0xA0)
				time.sleep(0.01)
				self.data(data)
			else:
				self.data(data)
