# Motion 생성

## cMotion 클래스(모터제어 개별 프로그램 이용)

+ cMotion.__init()__
  - 기능: cMotion 클래스 초기화

+ cMotion.set_profile(path)
  - 기능: 모터 프로파일을 설정합니다.
  - 매개변수
    + path: 모터 프로파일의 경로

+ cMotion.set_motor(no, position)
  - 기능: 모터 프로파일을 초기화합니다.

+ cMotion.set_motor(no, position)
  - 기능: 모터 1개를 특정 위치로 이동합니다.
  - 매개변수
    + no: 모터 번호
    + position: 모터 각도 (-80 ~ 80)

+ cMotion.set_motors(positions, movetime=None)
  - 기능: 전체 모터를 특정 위치로 이동합니다.
  - 매개변수
    + positions: 0-9번 모터 각도 배열 [...]
    + movetime: 모터 이동 시간(ms) - 50ms 단위, 모터가 정해진 위치까지 이동하는 시간(모터컨트롤러와의 overhead문제로 정밀하지는 않음)

+ cMotion.set_speed(no, speed)
  - 기능: 모터 1개의 속도를 변경합니다.
  - 매개변수
    + no: 모터 번호
    + speed: 모터 속도(0~255)

+ cMotion.set_acceleration(no, accel)
  - 기능: 모터 1개의 가속도를 변경합니다.
  - 매개변수
    + no: 모터번호
    + accel: 모터 가속도(0~255)

+ cMotion.get_motion()
  - 기능: 모션 프로파일를 조회합니다.
  - 반환값
    + data: 프로파일 객체

+ cMotion.set_motion(pname, cycle)
  - 기능: 모션 프로파일의 동작을 실행합니다.
  - 매개변수
    + pname: 모션 프로파일 이름
    + cycle: 모션 반복 횟수
  - 반환값
    + ret: 성공/실패

+ cMotion.stop()
  - 기능: 동작을 정지합니다.


## PyMotion 클래스(모터컨트롤러와 직접 통신)

+ PyMotion.__init()__
  - 기능: PyMotion 클래스를 초기화합니다.

+ PyMotion.set_motor(n, position)
  - 기능: 모터 1개를 특정 위치로 이동합니다.
  - 매개변수
    + no: 모터 번호
    + position: 모터 각도 (-80 ~ 80)
  - 반환값
    + ret: 성공/실패

+ PyMotion.set_motors(positions)
  - 기능: 전체 모터를 특정 위치로 이동합니다.
  - 매개변수
    + positions: 0-9번 모터각도 [...]
  - 반환값
    + ret: 성공/실패

+ PyMotion.set_speed(no, speed)
  - 기능: 모터 1개의 속도를 변경합니다.
  - 매개변수
    + no: 모터 번호
    + speed: 모터 속도(0~255)
  - 반환값
    + ret: 성공/실패

+ PyMotion.set_acceleration(no, accel)
  - 기능: 모터 1개의 가속도를 변경합니다.
  - 매개변수
    + no: 모터번호
    + accel: 모터 가속도(0~255)
  - 반환값
    + ret: 성공/실패

+ PyMotion.set_init()
  - 기능: 전체 모터를 초기 상태로 이동시킵니다.
