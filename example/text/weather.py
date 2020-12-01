import os
import sys
sys.path.append('/home/pi/openpibo/lib')

from text.textlib import cText
from audio.audiolib import cAudio

def tts_f():
  tObj = cText()
  #filename = "/home/pi/openpibo/data/tts.wav"
  filename = "weather.wav"
  tObj.tts("서울시 강남구  오늘 날씨를 알려줄게요. 맑씨는 맑음, 기온은 17도입니다.", filename)
  print(filename)
  aObj = cAudio()
  aObj.play(filename)

if __name__ == "__main__":
  tts_f()
