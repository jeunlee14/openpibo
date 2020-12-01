import sys
sys.path.append('/home/pi/openpibo/lib')

from oled.oledlib import cOled
from motion.motionlib import cMotion
from threading import Thread, Lock
import os

def move():
  m = cMotion()
  m.set_motion("speak1", 1)
  os.system('sudo servo init')


oObj = cOled()
oObj.set_font(size=20)
oObj.draw_image("../../data/clear.png")
oObj.draw_text((80,20), "맑음")
oObj.show()
Thread(target=move, args=()).start()

os.system('omxplayer -o local weather.wav')
oObj.clear()
oObj.show()
