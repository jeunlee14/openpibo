# Device 제어

## cDevice 클래스

+ cDevice.__init__(func)
  - 기능: cDevice 클래스를 초기화합니다.

+ cDevice.locked()
  - 기능: Device가 사용 중인지 확인한다.
  - 반환값
    + ret: True/False

+ cDevice.send_cmd(code, data)
  - 기능: Device에 메시지 코드/데이터를 전송하고 응답을 받습니다.
  - 매개변수
    + code: 메시지 코드
    + data: 메시지
  - 반환값
    + data:  Device 로부터 받은 응답

+ cDevice.send_raw(raw)
  - 기능: Device에 실제 메시지를 전송하고 응답을 받습니다.
  - 매개변수
    + raw: 실제 전달되는 메시지
  - 반환값
    + data:  Device 로부터 받은 응답


## 메시지 상세 설명

+ cDevice.VERSION 
  - get: 버전정보

+ cDevice.HALT
  - set: 전원종료 요청(데이터 필요없음)
  - get: 전원종료 통보

+ cDevice.DC_CONN
  - get: DC잭 연결정보 

+ cDevice.BATTERY
  - get: 배터리정보

+ cDevice.NEOPIXEL / data: 255,255,255
  - set: 네오픽셀설정 (R,G,B) 양쪽 동일하게 설정
  - get: "ok"

+ cDevice.NEOPIXEL_EACH / data: 255,255,255,255,255,255
  - set: 네오픽셀설정 (R,G,B,R,G,B) 양쪽 각각 설정
  - get: "ok"

+ cDevice.PIR / data: "on" or "off"
  - set: pir sensor "on"(활성화)/"off"(비활성화)

+ cDevice.TOUCH

+ cDevice.SYSTEM / data: (1)-(2)-(3)-(4)-(5)-(6)
  1. PIR 감지: "person" or "nobody"
  2. Touch 감지: "touch" or ""
  3. DC잭 연결감지: "on" of "off"
  4. 버튼 감지: "on" or ""
  5. 시스템리셋: not support
  6. 전원종료: "on" or ""


## 참고자료

+ 전체 메시지 리스트
  - MSG_TYPE_VERSION(10) ->  ex) #10:!
  - MSG_TYPE_HALT(11) -> ex) #11:!
  - MSG_TYPE_RESET(12) -> ex) #12:!
  - MSG_TYPE_BUTTON(13) -> ex) no Send
  - MSG_TYPE_DC_CONN(14) -> ex) #14:!
  - MSG_TYPE_BATTERY(15) -> ex) #15:!
  - MSG_TYPE_AUDIO_EN(16) -> ex) #16:!
  - MSG_TYPE_REBOOT(17) -> ex) #17:!
  - MSG_TYPE_NEOPIXEL(20) -> ex) #20:255,255,255!
  - MSG_TYPE_NEOPIXEL_FADE(21) -> ex) #21:255,255,255,10!
  - MSG_TYPE_NEOPIXEL_BRIGHTNESS(22) -> ex) #22:64!
  - MSG_TYPE_NEOPIXEL_EACH(23) -> ex) #23:255,255,255,255,255,255!
  - MSG_TYPE_NEOPIXEL_FADE_EACH(24) -> ex) #24:255,255,255,255,255,255,10!
  - MSG_TYPE_NEOPIXEL_LOOP(25) -> ex) #25:2!  2 -- about 1s
  - MSG_TYPE_NEOPIXEL_OFFSET_SET(26) -> ex) #26:255,255,255,255,255,255!
  - MSG_TYPE_NEOPIXEL_OFFSET_GET(27) -> ex) #27:!
  - MSG_TYPE_NEOPIXEL_EACH_ORG(28) -> ex) #28:255,255,255,255,255,255!
  - MSG_TYPE_PIR(30) -> ex) #30:!
  - MSG_TYPE_TOUCH(31) -> ex) no send
