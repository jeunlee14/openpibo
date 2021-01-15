import csv
import random
#import io
import json
import os
from konlpy.tag import Mecab
import requests
from google_trans_new import google_translator
#from google.cloud import speech
#from google.cloud.speech import enums
#from google.cloud.speech import types

def getDiff(aT, bT):
  cnt = 0
  for i in aT:
    for j in bT:
      if i == j:
        cnt += 1
  return cnt / len(aT)

class cSpeech:
  def __init__(self, conf=None):
    self.translator = google_translator()
    self.kakao_account = conf.KAKAO_ACCOUNT

  def translate(self, string, to='ko'):
    return self.translator.translate(string, lang_tgt=to)

  def tts(self, string, filename="tts.mp3", lang="ko"):
    '''curl -v "https://kakaoi-newtone-openapi.kakao.com/v1/synthesize" \
    -H "Content-Type: application/xml" \
    -H "Authorization: KakaoAK API_KEY" \
    -d '<speak> 그는 그렇게 말했습니다.
    <voice name="MAN_DIALOG_BRIGHT">잘 지냈어? 나도 잘 지냈어.</voice>
    <voice name="WOMAN_DIALOG_BRIGHT" speechStyle="SS_ALT_FAST_1">금요일이 좋아요.</voice> </speak>' > result.mp3'''
    url = "https://kakaoi-newtone-openapi.kakao.com/v1/synthesize"
    headers = {
      'Content-Type': 'application/xml',
      'Authorization': 'KakaoAK ' + self.kakao_account
    }
    r = requests.post(url, headers=headers, data=string.encode('utf-8'))
    with open(filename, 'wb') as f:
      f.write(r.content)

  def stt(self, filename="stream.wav", lang="ko-KR"'''en-US''', timeout=5):
    cmd = "arecord -D dmic_sv -c2 -r 16000 -f S32_LE -d {} -t wav -q -vv -V streo stream.raw;sox stream.raw -c 1 -b 16 stream.wav;rm stream.raw".format(timeout)
    os.system(cmd)

    '''curl -v "https://kakaoi-newtone-openapi.kakao.com/v1/recognize" \
    -H "Transfer-Encoding: chunked" -H "Content-Type: application/octet-stream" \
    -H "Authorization: KakaoAK API_KEY" \
    --data-binary @stream.wav '''

    url = 'https://kakaoi-newtone-openapi.kakao.com/v1/recognize'
    headers = {
      'Content-Type': 'application/octet-stream',
      'Authorization': 'KakaoAK ' + self.kakao_account
    }

    data = open(filename, 'rb').read()
    res = requests.post(url, headers=headers, data=data)
    result_json_string = res.text[res.text.index('{"type":"finalResult"'):res.text.rindex('}')+1]
    result = json.loads(result_json_string)
    return result['value']

class cDialog:
  #"dialog_path":"/home/pi/openpibo/lib/text/data/dialog.csv"
  def __init__(self, conf=None):
    self.dialog_path = conf.PROC_PATH+"/dialog.csv"
    self.mecab = Mecab()
    self.dialog_db = []
    with open(self.dialog_path, 'r', encoding='utf-8') as f:
      rdr = csv.reader(f)
      self.dialog_db = [[self.mecab_morphs(line[0]), line[1], line[2]]for line in rdr]

  # mecab function
  def mecab_pos(self, string):
    return self.mecab.pos(string)

  def mecab_morphs(self, string):
    return self.mecab.morphs(string)

  def mecab_nouns(self, string):
    return self.mecab.nouns(string)

  def get_dialog(self, q):
    max_acc = 0
    max_ans = []
    c = self.mecab_morphs(q)
    for line in self.dialog_db:
      acc = getDiff(line[0], c)

      if acc == max_acc:
        max_ans.append(line)

      if acc > max_acc:
        max_acc = acc
        max_ans = [line]

    return random.choice(max_ans)[1]
