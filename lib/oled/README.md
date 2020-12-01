# OLED 제어

## cOled 클래스

+ cOled.__init__()
  - 기능: cOled 클래스를 초기화.

+ cOled.set_font(filename, size)
  - 기능: oled에 사용할 폰트 설정
  - 매개변수
    + filename: 폰트 파일 이름
    + size: 폰트 사이즈

+ cOled.draw_text(points, text)
  - 기능: 문자 그리기(한글, 영어 지원)
  - 매개변수
    + points: 문자열의 좌측/상단 좌표 튜플(x, y)
    + text: 문자열 내용

+ cOled.draw_image(filename)
  - 기능: 그림 그리기(128x64 png파일)
  - 매개변수
    + filename: 그림파일 경로

+ cOled.draw_rectangle(points, fill)
  - 기능: 사각형 그리기
  - 매개변수
    + points: 사각형의 좌측/상단 좌표, 사각형의 우측/하단 좌표 튜플(x,y,x1,y1)
    + fill: 채움

+ cOled.draw_ellipse(points, fill)
  - 기능: 원 그리기
  - 매개변수
    + points: 원을 둘러 싼 사각형의 좌측/상단 좌표, 사각형의 우측/하단 좌표 튜플(x,y,x1,y1)
    + fill: 채움

+ cOled.draw_line(points)
  - 기능: 선 그리기
  - 매개변수
    + points: 선의 시작 좌표, 선의 끝 좌표 (x,y,x1,y1)

+ cOled.invert()
  - 기능: 이미지 반전시키기

+ cOled.show()
  - 기능: 화면에 표시하기

+ cOled.clear()
  - 기능: 화면 지우기
