import argparse
import sys
sys.path.append('/home/pi/openpibo/lib')

from oled.oledlib import cOled

class Config:
  OPENPIBO_PATH="/home/pi/openpibo"
  OPENPIBO_DATA_PATH="/home/pi/openpibo-data"
  TESTDATA_PATH =OPENPIBO_DATA_PATH+"/testdata"
  PROC_PATH =OPENPIBO_DATA_PATH+"/proc"
  MODEL_PATH=OPENPIBO_DATA_PATH+"/models"

def disp(args):
  o = cOled(conf=Config())
  o.set_font(size=12)
  o.draw_text((0, 0), "# NETWORK")
  o.draw_text((0,15), "[E]: {}".format(args.eip))
  o.draw_text((0,30), "[S]: {}".format(args.ssid))
  o.draw_text((0,45), "[W]: {}".format(args.wip))
  o.show()


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--eip', help='eth ip address', required=True)
  parser.add_argument('--wip', help='wlan0 ip address', required=True)
  parser.add_argument('--ssid', help='wlan0', required=True)
  args = parser.parse_args()
  disp(args)
