import time
import pprint
import sys
sys.path.append('/home/pi/openpibo/lib')

from motion.motionlib import cMotion

if __name__ == "__main__":
  m = cMotion()
  data = m.get_motion()
  pprint.pprint(data)
  m.set_motion("hand1", 3)
  print("end") 
