import serial
import time
from threading import Lock

class cDevice:
  def __init__(self):
    self.code = {
    "VERSION":"10",
    "HALT":"11",
    "BUTTON":"13",
    "DC_CONN":"14",
    "BATTERY":"15",
    "NEOPIXEL":"20",
    "NEOPIXEL_EACH":"23",
    "PIR":"30",
    "TOUCH":"31",
    "SYSTEM":"40",
    }
    self.dev = serial.Serial(port="/dev/ttyS0", baudrate=9600)
    self.lock = Lock()

  def locked(self):
    return self.lock.locked()

  def send_cmd(self, code, data=""):
    return self.send_raw("#{}:{}!".format(code, data))

  def send_raw(self, raw):
    if self.lock.locked() == True:
      return False

    self.lock.acquire()
    self.dev.write(raw.encode('utf-8'))
    data = ""
    time.sleep(0.05)
    while True:
      ch = self.dev.read().decode()
      if ch == '#' or ch == '\r' or ch == '\n':
        continue
      if ch == '!':
        break
      data += ch
    self.lock.release()
    return data
