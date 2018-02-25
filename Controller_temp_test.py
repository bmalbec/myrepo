import time
import serial
import struct
import xml.etree.ElementTree as ET
import math
import re
from shutil import copyfile

ser = serial.Serial('/dev/ttyO4', 38400, timeout=0.15)
time.sleep(0.01)

mybackup = open("testfile5.xml",'r')
backup = mybackup.read()
mybackup2 = open("testfile6.xml",'w')
cover = mybackup2.write(backup)
mybackup.close()
mybackup2.close()

tempTemplate = open("temp_xml_
