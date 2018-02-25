import time
import serial
import struct
import xml.etree.ElementTree as ET
import math
import re
from shutil import copyfile
from US2066 import US2066Base as DISP

ser = serial.Serial('/dev/ttyO4', 38400, timeout=0.15)
time.sleep(0.01)

disp = DISP(0x3C)

disp.begin()

time.sleep(0.01)

disp.command(0x01)
time.sleep(0.001)

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
    tempXmlBackup.close()
  if not tempSerialData:
    tempSerialData2 = open("temp_xml_backup.xml", 'r')
    tempSerialData = tempSerialData2.read()
    tempSerialData2.close()

  tempXmlData.write(tempSerialData)

  tempXmlData.close()
  time.sleep(0.01)
  tempXmlTree = ET.parse("temp_xml_data.xml")
  tempXmlRoot = tempXmlTree.getroot()

  temp = tempXmlRoot[0][0].text
  print(temp)
  disp.write(temp)
