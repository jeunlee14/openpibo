import serial
import time
from threading import Thread, Lock

MESSAGE = {
"10":"VERSION",
"11":"HALT",
"13":"BUTTON",
"14":"DC_CONN",
"15":"BATTERY",
"20":"NEOPIXEL",
"23":"NEOPIXEL_EACH",
"30":"PIR",
"31":"TOUCH",
"40":"SYSTEM",
}

class cDevice:
  _defaults = {
    "DEVICE_PATH":"/dev/ttyS0",
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

  def __init__(self, func=None):
    self.__dict__.update(self._defaults) # set up default values
    self.dev = serial.Serial(port=self.DEVICE_PATH, baudrate=9600)
    self.func = func
    self.stopped = False
    self.system_check_time = 0
    self.battery_check_time = 0
    self.lock = Lock()
    self.next_cmd = [False, ""]

  def start(self):
    t = Thread(target=self.update, args=())
    t.daemon = True
    t.start()
    return self

  def update(self):
    self.system_check_time = time.time()
    self.battery_check_time = time.time()
    while True:
      if self.stopped:
        return

      if self.next_cmd[0] == True:
        self.send_raw(self.next_cmd[1])

      if time.time() - self.system_check_time > 1:
        self.send_cmd(self.SYSTEM)
        self.system_check_time = time.time()

      if time.time() - self.battery_check_time > 10:
        self.send_cmd(self.BATTERY)
        self.battery_check_time = time.time()

      time.sleep(0.1)

  def stop(self):
    self.stopped = True

  def get_type(self, code):
    return MESSAGE.get(code)

  def get_command_list(self):
    return MESSAGE

  def send_cmd(self, code, data=""):
    return self.send_raw("#{}:{}!".format(code, data))

  def send_raw(self, raw):
    if self.lock.locked() == True:
      self.next_cmd = [True, raw]
      return

    self.next_cmd = [False, ""]
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
    if self.func is not None:
      self.func(data)

    self.lock.release()
    return data
