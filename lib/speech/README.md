# Speech 제어

## cSpeech 클래스 

+ cSpeech.__init()__
  - 기능: cSpeech 클래스를 초기화합니다.
  - 매개변수
    + google_account: 구글 계정 json파일 경로

+ cSpeech.translate(string, src, dest)
  - 기능: 구글 번역기를 이용해서 문장을 번역합니다.
  - 매개변수
    + string: 번역할 문장
    + src: 입력할 언어타입('en', 'ko' ..)
    + dest: 번역될 언어타입('en', 'ko' ..)
  - 반환값
    + data: 번역된 문장

+ cSpeech.tts(string, filename, lang)
  - 기능: TTS(Speech to Speech)/ Speech(문자)를 Speech(말)로 변환합니다.
  - 매개변수
    + string: 변환할 문장
    + filename: 저장할 파일이름(wav)
    + lang: 한글ko or 영어en

+ cSpeech.stt(filename, timeout)
  - 기능: STT(Speech to Speech)/ Speech(말)을 Speech(문자)로 변환합니다.
  - 매개변수
    + filename: 저장할 파일이름(flac)
    + timeout: 녹음할 시간(초)
  - 반환값
    + ret: 성공/실패


## cDialog 클래스

+ cDialog.__init(dialog_path)__
  - 기능: cDialog 클래스를 초기화합니다.
  - 매개변수
    + dialog_path: dialog csv파일 path

+ cDialog.mecab_pos(string)
  - 기능: 형태소를 pos모드로 추출합니다.
  - 매개변수
    + string: 분석할 문장(한글)
  - 반환값
    + data: 분석한 결과

+ cDialog.mecab_morphs(string)
  - 기능: 형태소를 morphs모드로 추출합니다.
  - 매개변수
    + string: 분석할 문장(한글)
  - 반환값
    + data: 분석한 결과

+ cDialog.mecab_nouns(string)
  - 기능: 명사를 추출합니다.
  - 매개변수
    + string: 분석할 문장(한글)
  - 반환값
    + data: 분석한 결과

+ cDialog.get_dialog(q)
  - 기능: 초기버전의 일상대화에 대한 답을 추출합니다.
  - 매개변수
    + q: 질문(한글)
  - 반환값
    + data: 대답


# 참고
# https://blog.naver.com/PostView.nhn?blogId=kkyy0126&logNo=221476967829&from=search&redirect=Log&widgetTypeCall=true&directAccess=false

