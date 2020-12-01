import os
import sys
sys.path.append('/home/pi/openpibo/lib')

from speech.speechlib import cSpeech

obj = cSpeech(google_account="/home/pi/piboproject-d783ed0496cb.json")
ret = obj.stt(lang="en-US")
print(ret)
