import time
import pprint
import sys
sys.path.append('/home/pi/openpibo/lib')

from motion.motionlib import cPyMotion

if __name__ == "__main__":
  m = cPyMotion()
  print(m.set_speed(2, 50))
  print(m.set_acceleration(2, 0))
  time.sleep(0.5)
  print(m.set_motor(2, 30))
  time.sleep(0.5)
  print(m.set_motor(2, -30))
  time.sleep(0.5)
  print('end')
