import sys
sys.path.append('/home/pi/openpibo/lib')

from text.textlib import cDialog

# chatbot 관련 처리 함수
import chatlib
db = {
  "날씨":{
    "내일":chatlib.weather,
    "오늘":chatlib.weather,
    "어제":chatlib.weather,
  },
  "음악":{
    "발라드":chatlib.music, 
    "락"    :chatlib.music,
    "힙합"  :chatlib.music,
  },
  "뉴스":{
    "경제":chatlib.news,
    "기술":chatlib.news,
    "연예":chatlib.news,
  },
}

def main():
  obj = cDialog()
  print("대화 시작합니다.")
  while True:
    c = input("입력 > ")
    matched = False
    if c == "그만":
      break

    d = obj.mecab_morphs(c)
    #print("형태소 분석: ", d)
    for key in db.keys():
      if key in d:
        for key1 in db[key].keys():
          if key1 in d:
            db[key][key1](key1)
            matched = True

    if matched == False:
      print("대화봇 > ", obj.get_dialog(c))

if __name__ == "__main__":
  main()
