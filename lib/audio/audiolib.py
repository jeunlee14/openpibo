import os

class cAudio:
  # out: local/hdmi/both
  # volume: mdB
  # filename: mp3/wav
  def play(self, filename, out='local', volume='-2000'):
    os.system("omxplayer -o {} --vol {} {} &".format(out, volume, filename))

  def stop(self):
    os.system('sudo pkill omxplayer')
