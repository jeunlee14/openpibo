import sys
sys.path.append('/home/pi/openpibo/lib')

from speech.speechlib import cSpeech

def translate_f():
  obj = cSpeech()
  string = "안녕하세요"
  ret = obj.translate(string, src="ko", dest="en")
  print("Input:", string)
  print("Output:", ret)

if __name__ == "__main__":
  translate_f()
