import Adafruit_BBIO.ADC as ADC
import time
import sys
import serial
import struct
import xml.etree.ElementTree as ET
import math
import signal

tempPin = "AIN1"

ser = serial.Serial('/dev/ttyO4', 38400)

ADC.setup()
time.sleep(0.01)

while (True):
  rawTemp = ADC.read(tempPin)
  time.sleep(2)
  
  tempData = ET.Element('data')
    tempItem = ET.SubElement(tempData, 'temp')
    tempItem1 = ET.SubElement(tempItem, 'item')
    tempItem1.set('name','Temperature')
    tempItem1.text = rawTemp
  
  tempXML = ET.tostring(tempData)
    ser.write(tempXML)
    ser.write('\n')
  
  print("Wrote ", rawTemp, " to UART\n"
