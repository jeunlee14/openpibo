import os
import time
import sys
sys.path.append('/home/pi/openpibo/lib')

from audio.audiolib import cAudio

def tts_f():
  obj = cAudio()
  obj.set_config(out="local", volume=-2500)
  print(obj.get_config())
  obj.play("/home/pi/openpibo/data/test.mp3")
  time.sleep(5)
  obj.stop()
if __name__ == "__main__":
  tts_f()
