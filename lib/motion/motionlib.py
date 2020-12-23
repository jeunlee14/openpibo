import serial
import time
import os
import json

class cMotion:
  #"profile_path":"/home/pi/openpibo/lib/motion/motion_db.json"
  def __init__(self, conf=None):
    self.profile_path=conf.PROC_PATH+"/motion_db.json"
    with open(self.profile_path, 'r') as f:
      self.profile = json.load(f)

  def set_profile(self, path):
    with open(path, 'r') as f:
      self.profile = json.load(f)

  def set_motor(self, no, position):
    os.system("servo write {} {}".format(no, position*10))

  def set_motors(self, positions, movetime=None): # pos array
    mpos = [positions[i]*10 for i in range(len(positions))]
    
    if movetime == None:
      os.system("servo mwrite {}".format(" ".join(map(str, mpos))))
    else:
      os.system("servo move {} {}".format(" ".join(map(str, mpos)), movetime))
    return True

  def set_speed(self, n, spd):
    os.system("servo speed {} {}".format(n, spd))

  def set_acceleration(self, n, accl):
    os.system("servo accelerate {} {}".format(n, accl))

  def get_motion(self, name):
    ret = self.profile.get(name)
    ret = self.profile if ret == None else ret
    return ret

  def set_motion(self, name, cycle=1):
    ret = True
    exe = self.profile.get(name)

    if exe == None:
      ret = False
      print("profile not exist", name)
    else:
      seq,cnt,cycle_cnt = 0,0,0
      self.stopped = False

      while True:
        if self.stopped:
          break

        d, intv = exe["pos"][cnt]["d"], exe["pos"][cnt]["seq"]-seq
        seq = exe["pos"][cnt]["seq"]

        self.set_motors(d, intv)
        time.sleep(intv/1000)
        cnt += 1
        if cnt == len(exe["pos"]):
          cycle_cnt += 1
          if cycle > cycle_cnt:
            cnt,seq = 0,0
            continue
          break
    return ret

  def stop(self):
    self.stopped = True

class cPyMotion:
  _defaults = {
    "device_path":"/dev/ttyACM0",
  }

  def __init__(self):
    self.__dict__.update(self._defaults) # set up default values
    self.dev = serial.Serial(port=self.device_path, baudrate=115200)
    self.motor_range = [25,35,80,30,50,25,25,35,80,30]

  def set_motor(self, n, degree):
    ret = True

    if abs(degree) > self.motor_range[n]:
      return False, "range error ch:{} range:-{} ~ {}".format(n, -1*self.motor_range[n], self.motor_range[n])

    pos = (degree*10 + 1500)*4
    lsb = pos & 0x7f #7 bits for least significant byte
    msb = (pos >> 7) & 0x7f #shift 7 and take next 7 bits for msb
    cmd = chr(0x84) + chr(n) + chr(lsb) + chr(msb)
    self.dev.write(bytes(cmd,'latin-1'))
    return ret, ""

  def set_motors(self, d_lst): # pos array
    ret = True

    for i in range(len(d_lst)):
      if abs(d_lst[i]) > self.motor_range[i]:
        return False, "range error ch:{} range:-{} ~ {}".format(i, -1*self.motor_range[i], self.motor_range[i])

    p_lst = [(d_lst[i]*10+1500)*4 for i in range(len(d_lst))]
    cmd = chr(0x9F) + chr(10) + chr(0)
    for pos in p_lst:
      lsb = pos & 0x7f #7 bits for least significant byte
      msb = (pos >> 7) & 0x7f #shift 7 and take next 7 bits for msb
      cmd += chr(lsb) + chr(msb)
    self.dev.write(bytes(cmd,'latin-1'))
    return ret, ""

  def set_speed(self, n, val):
    ret = True

    if abs(val) > 255:
      return False, "range error range: 0~255"

    lsb = val & 0x7f #7 bits for least significant byte
    msb = (val >> 7) & 0x7f #shift 7 and take next 7 bits for msb
    cmd = chr(0x87) + chr(n) + chr(lsb) + chr(msb)
    self.dev.write(bytes(cmd,'latin-1'))
    return ret, ""

  def set_acceleration(self, n, val):
    ret = True

    if abs(val) > 255:
      return False, "range error range: 0~255"

    lsb = val & 0x7f #7 bits for least significant byte
    msb = (val >> 7) & 0x7f #shift 7 and take next 7 bits for msb
    cmd = chr(0x89) + chr(n) + chr(lsb) + chr(msb)
    self.dev.write(bytes(cmd,'latin-1'))
    return ret, ""

  def set_init(self):
    ret = True
    cmd = chr(0xA2)
    self.dev.write(bytes(cmd,'latin-1'))
    return ret, ""
