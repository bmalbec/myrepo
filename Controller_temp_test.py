import time
import serial
import struct
import xml.etree.ElementTree as ET
import math
import re
from shutil import copyfile
from US2066 import US2066Base as DISP

def oled_init(display):
  display.command(0x01)
  display.command(0x00)
  display.write("Temperature:")
  
def oled_temp(display, temperature)
  display.command(0xA0)
  display.write(temperature)
  
ser = serial.Serial('/dev/ttyO4', 38400, timeout=0.15)
time.sleep(0.01)

disp = DISP(0x3C)

disp.begin()

time.sleep(0.01)

oled_init(disp)
time.sleep(0.001)

tempOldSerialInit = open("temp_xml_template.xml", 'r')
tempOldSerialData = tempOldSerialInit.read()
tempOldSerialInit.close()

while (True):
  tempXmlTemplate = open("temp_xml_template.xml", 'r')
  tempXmlBackup = tempXmlTemplate.read()
  tempXmlBackup2 = open("temp_xml_backup.xml", 'w+')
  tempCover = tempXmlBackup2.write(tempXmlBackup)
  tempXmlTemplate.close()
  tempXmlBackup2.close()

  tempXmlData = open("temp_xml_data.xml", 'w+')
  tempSerialData = ser.readline()
  if tempSerialData:
    tempXmlBackup = open("temp_xml_backup.xml", 'w')
    tempXmlBackup.write(tempSerialData)
    tempOldSerialData = tempSerialData
    tempXmlBackup.close()
  if not tempSerialData:
    tempSerialData = tempOldSerialData

  tempXmlData.write(tempSerialData)

  tempXmlData.close()
  time.sleep(0.01)
  tempXmlTree = ET.parse("temp_xml_data.xml")
  tempXmlRoot = tempXmlTree.getroot()

  temp = tempXmlRoot[0][0].text
  print(temp)
  oled_temp(disp, temp)
  time.sleep(1)
