import csv
import random
#import io
import json
import os
from konlpy.tag import Mecab
import requests
from speech.google_trans_new import google_translator
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
    '''curl -v -X POST "https://dapi.kakao.com/v2/translation/translate" \
    -d "src_lang=kr" \
    -d "target_lang=en" \
    --data-urlencode "query=지난해 3월 오픈한 카카오톡 주문하기는 현재까지 약 250만명의 회원을 확보했으며, 주문 가능한 프랜차이즈 브랜드는 38개, 가맹점수는 약 1만 5천여곳에 달한다. 전 국민에게 친숙한 카카오톡 UI를 활용하기 때문에 남녀노소 누구나 쉽게 이용할 수 있으며, 별도의 앱을 설치할 필요 없이 카카오톡 내에서 모든 과정이 이뤄지는 것이 특징이다. 지난해 9월 업계 최초로 날짜와 시간을 예약한 뒤 설정한 매장에서 주문 음식을 찾아가는 ‘픽업’ 기능을 도입했고, 올해 1월 스마트스피커 ‘카카오미니’에서 음성을 통해 주문 가능한 메뉴를 안내받을 수 있도록 서비스를 연동하며 차별화를 꾀했다. 중소사업자들이 카카오톡 주문하기에 입점하게 되면 4,300만 카카오톡 이용자들과의 접점을 확보하고, 간편한 주문 과정으로 만족도를 높일 수 있게 된다. 카카오톡 메시지를 통해 신메뉴 출시, 프로모션 등의 소식을 전달할 수 있고, 일대일 채팅 기능을 적용하면 고객과 직접 상담도 가능하다." \
    -H "Authorization: KakaoAK {REST_API_KEY}"'''

    '''
    # kakao translate source
    url = 'https://dapi.kakao.com/v2/translation/translate'
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Authorization': 'KakaoAK ' + self.kakao_account
    }

    res = requests.post(url, headers=headers, data={"src_lang":"kr", "target_lang":"en", "query":string})
    try:
      result = {"result":True, "value":json.loads(res.text)["translated_text"]}

    except Exception as ex:
      result = {"result":False, "value":""}
    return result['value']'''
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

  def stt(self, filename="stream.wav", timeout=5):
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
    try:
      result_json_string = res.text[res.text.index('{"type":"finalResult"'):res.text.rindex('}')+1]
    except Exception as ex:
      result_json_string = res.text[res.text.index('{"type":"errorCalled"'):res.text.rindex('}')+1]
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
