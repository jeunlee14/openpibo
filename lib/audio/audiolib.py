import os

class cAudio:
  _defaults = {
    "out":"local",
    "volume":0
  }

  def __init__(self):
    self.__dict__.update(self._defaults) # set up default values

  def set_config(self, out="local", volume=0):
    # out: local/hdmi/both
    self.out = out
    self.volume = volume

  def get_config(self):
    return {"out":self.out, "volume":self.volume}

  def play(self, filename): # mp3/wav
    os.system("omxplayer -o {} --vol {} {} &".format(self.out, self.volume, filename))

  def stop(self):
    os.system('sudo pkill omxplayer')
