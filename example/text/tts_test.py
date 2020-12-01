import os
import sys
sys.path.append('/home/pi/openpibo/lib')

from text.textlib import cText
from audio.audiolib import cAudio

def tts_f():
  tObj = cText()
  filename = "/home/pi/openpibo/data/tts.mp3"
  tObj.tts("지금 몇 시에요?", filename)
  print(filename)
  aObj = cAudio()
  aObj.set_config(volume=-2500)
  aObj.play(filename)

if __name__ == "__main__":
  tts_f()
