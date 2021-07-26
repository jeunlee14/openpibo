import os

HIGH = 1
LOW = 0

class cAudio:
  # out: local/hdmi/both
  # volume: mdB
  # filename: mp3/wav
  def __init__(self):
    os.system('gpio mode 7 out')
    os.system(f'gpio write 7 {HIGH}')

  def play(self, filename, out='local', volume='-2000', background=True):
    if background:
      os.system("omxplayer -o {} --vol {} {} &".format(out, volume, filename))
    else:
      os.system("omxplayer -o {} --vol {} {}".format(out, volume, filename))

  def stop(self):
    os.system('sudo pkill omxplayer')
  
  def mute(self, value):
    if type(value) != bool:
      raise TypeError(f"'{value}' is not a bool.")
    if value:
      os.system(f'gpio write 7 {LOW}')
    else:
      os.system(f'gpio write 7 {HIGH}')