import sys
sys.path.append('/home/pi/openpibo/lib')

from motion.motionlib import cMotion

m = cMotion()
m.set_motion("wave1", 2)
#m.set_motion("forward1", 1)
#m.set_motion("greeting", 1)
