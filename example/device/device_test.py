'''
+ 메시지 구조
 - VERSION(10) ->  ex) #10:!
 - HALT(11) -> ex) #11:!
 - DC_CONN(14) -> ex) #14:!
 - BATTERY(15) -> ex) #15:!
 - PIR(30) -> ex) #30:!
 - TOUCH(31) -> ex) #31:!
'''
import time
import sys
sys.path.append('/home/pi/openpibo/lib')

from device.devicelib import cDevice

def my_func(s):
  print("===========================")
  print("Result: ", s)
  arr = s.split(':')
  print(" ({}/{})".format(obj.get_type(arr[0]), arr[1]))
  print("===========================")

if __name__ == "__main__":
  obj = cDevice(my_func).start()
  obj.send_cmd(obj.VERSION)
  obj.send_cmd(obj.PIR, "on")

  while True:
    pkt = input("")
    
    if pkt == 'q':
      break
    obj.send_raw(pkt)
