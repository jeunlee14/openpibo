import os

HIGH = 1
LOW = 0

class cAudio:
  # out: local/hdmi/both
  # volume: mdB
  # filename: mp3/wav

  def __init__(self):
    self.is_mute = HIGH
    os.system('gpio mode 7 out')
    os.system('gpio write 7 1')

  def play(self, filename, out='local', volume='-2000', background=True):
    if background:
      os.system("omxplayer -o {} --vol {} {} &".format(out, volume, filename))
    else:
      os.system("omxplayer -o {} --vol {} {}".format(out, volume, filename))

  def stop(self):
    os.system('sudo pkill omxplayer')
  
  def mute(self):
    if self.is_mute == HIGH:
      self.is_mute = LOW
    else:
      self.is_mute = HIGH
    os.system(f'gpio write 7 {self.is_mute}')