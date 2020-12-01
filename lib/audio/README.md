# Audio 제어

## cAudio 클래스

+ cAudio.__init()__:
  - 기능: cAudio 클래스를 초기화합니다.
  - 초기화
    + 출력대상 초기화 out = "local"
    + 볼륨 초기화 volume = 0

+ cAudio.set_config(out, volume)
  - 기능: 오디오의 출력대상 및 볼륨을 설정합니다.
  - 매개변수
    + out: 출력대상(local/hdmi/both), local(3.5mm잭) / hdmi
    + volume: 음량 단위: 1/1000 ㏈

+ cAudio.get_config()
  - 기능: 오디오의 관련 설정을 확인합니다.
  - 반환값
    + ret: {"out": 출력대상, "volume": 음량크기}

+ cAudio.play(filename)
  - 기능: mp3 또는 wav 파일을 재생합니다.
  - 매개변수
    + filename: 재생할 파일(mp3)

+ cAudio.stop()
  - 기능: 오디오 재생을 정지합니다.
