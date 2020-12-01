import time
import sys
sys.path.append('/home/pi/openpibo/lib')
from device.devicelib import cDevice

obj = cDevice()
data = obj.send_raw("#20:30,140,160!")
time.sleep(1)
data = obj.send_raw("#20:0,0,0!")
time.sleep(1)
data = obj.send_raw("#20:30,140,160!")
time.sleep(1)
data = obj.send_raw("#20:0,0,0!")
time.sleep(1)
data = obj.send_raw("#20:30,140,160!")
time.sleep(1)
data = obj.send_raw("#20:0,0,0!")
time.sleep(1)
data = obj.send_raw("#20:30,140,160!")
time.sleep(1)
data = obj.send_raw("#20:0,0,0!")
time.sleep(1)
data = obj.send_raw("#20:30,140,160!")
time.sleep(1)
data = obj.send_raw("#20:0,0,0!")
time.sleep(1)
data = obj.send_raw("#20:30,140,160!")
time.sleep(1)
data = obj.send_raw("#20:0,0,0!")


