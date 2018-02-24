import Adafruit_BBIO.ADC as ADC
import time

tempPin = "AIN1"

ADC.setup()
time.sleep(0.01)
while (True):
  print(ADC.read(tempPin))
