import time
import sys
sys.path.append('/home/pi/openpibo/lib')

from oled.oledlib import cOled

def oled_f():
  oObj = cOled()
  oObj.set_font(size=10)
  oObj.draw_image("../../data/clear.png")
  oObj.draw_text((70,20), "Hello World")
  oObj.draw_rectangle((30,30,40,40) ,True)
  oObj.show()
  time.sleep(5)
  oObj.clear()
  oObj.show()

if __name__ == "__main__":
  oled_f()
