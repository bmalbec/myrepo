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
		"0":0x20,
		"1":0x21,
		"2":0x22,
		"3":0x23,
		"4":0x24,
		"5":0x25,
		"6":0x26,
		"7":0x27,
		"8":0x28,
		"9":0x29,
		":":0x2A,
		";":0x2B,
		"<":0x2C,
		"=":0x2D,
		">":0x2E,
		"?":0x2F,
		"|":0x30,
		"A":0x31,
		"B":0x32,
		"C":0x33,
		"D":0x34,
		"E":0x35,
		"F":0x36,
		"G":0x37,
		"H":0x38,
		"I":0x39,
		"J":0x3A,
		"K":0x3B,
		"L":0x3C,
		"M":0x3D,
		"N":0x3E,
		"O":0x3F,
		"P":0x40,
		"Q":0x41,
		"R":0x42,
		"S":0x43,
		"T":0x44,
		"U":0x45,
		"V":0x46,
		"W":0x47,
		"X":0x48,
		"Y":0x49,
		"Z":0x4A
		
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
			self.data(hex(data))


disp = US2066Base(0x3C)

disp.begin()

text1 = ["h","e","l","l","o"]

time.sleep(0.01)

disp.command(0x01)
time.sleep(0.001)
disp.write("IT WORKS")
disp.command(0xA0)

