# Audio 제어

## cAudio 클래스
+ cAudio.play(out, volume, filename, background)
  - 기능: mp3 또는 wav 파일을 재생합니다.
  - 매개변수
    + filename: 재생할 파일(mp3)
    + out: 출력대상(local/hdmi/both), local(3.5mm잭) / hdmi
    + volume: 음량 단위: 1/1000 ㏈
    + background: (True/False) 백그라운드모드로 실행 여부(default: True)

+ cAudio.stop()
  - 기능: 오디오 재생을 정지합니다.
