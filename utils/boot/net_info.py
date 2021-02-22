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
  v = args.eip.split(",") + args.wip.split(",")
  o = cOled(conf=Config())
  o.set_font(size=12)

  eip = v[1] if v[0] == "" else v[0]
  wip = v[4] if v[2] == "" else v[2]
  ssid = v[5] if v[3] == "" else v[3]

  o.draw_text((0,0), "# NETWORK")
  o.draw_text((0,15), "[EIP]:{}".format(eip))
  o.draw_text((0,30), "[WIP]:{}".format(wip))
  o.draw_text((0,45), "[SSID]:{}".format(ssid))

  o.show()


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--eip', help='eth ip address', required=True)
  parser.add_argument('--wip', help='wlan ip address', required=True)
  args = parser.parse_args()
  disp(args)
