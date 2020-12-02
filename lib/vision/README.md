# Computer Vision

## cCamera 클래스

+ 기능
  - 사진 촬영,읽기,쓰기,보기 등 카메라 기본 기능
  - 스트리밍, Cartoonize 기능
  - 이미지에 사각형/글씨 입력 

+ cCamera.__init__()
  - 기능: cCamera 클래스를 초기화 합니다.

+ cCamera.imread(filename)
  - 기능: 이미지 파일을 읽습니다.
  - 매개변수
    + filename: 사용할 이미지 파일
  - 반환값
    + ret: 이미지 객체

+ cCamera.read(w, h)
  - 기능: 카메라를 통해 이미지를 촬영합니다.
  - 매개변수
    + w: 사진의 width 값 (default:640)
    + h: 사진의 height 값 (default:480)
  - 반환값
    + ret: 촬영한 이미지 객체

+ cCamera.imwrite(filename, img)
  - 기능: 이미지를 파일로 저장합니다.
  - 매개변수
    + filename: 저장할 파일이름
    + img: 저장할 이미지 객체(imread or read로 얻은 이미지 객체)

+ cCamera.imshow(img, title)
  - 기능: 모니터에서 이미지를 확인합니다.(GUI 환경에서만 동작)
  - 매개변수
    + img: 보여줄 이미지
    + title: 사진 윈도우의 제목

+ cCamera.waitKey(timeout)
  - 기능: 이미지를 보는 시간(show함수와 함께 사용합니다.)
  - 매개변수
    + timeout: 지연시간(ms)

+ cCamera.streaming(w, h, timeout)
  - 기능: 모니터에서 이미지를 스트리밍합니다.(GUI 환경에서만 동작)
  - 매개변수
    + w: 사진의 width 값 (default:640)
    + h: 사진의 height 값 (default:480)
    + timeout: 스트리밍 시간 (default:5초)

+ cCamera.rectangle(img, p1, p2, color, tickness)
  - 기능: 이미지에 네모를 그립니다.
  - 매개변수
    + img: imread or read함수의 결과 (이미지 데이터)
    + p1: 좌측상단 좌표(x, y)
    + p2: 우측하단 좌표(x, y)
    + color: RGB값 (r,g,b)
    + tickness: 굵기

+ cCamera.putText(img, text, p, size, color, tickness)
  - 기능: 이미지에 문자를 입력합니다.
  - 매개변수
    + img: imread or read함수의 결과 (이미지 데이터)
    + text: 표시할 문자열
    + p: 좌측상단 좌표(x, y)
    + size: 
    + color: RGB값 (r,g,b)
    + tickness: 굵기

+ cCamera.cartoonize(img)
  - 기능: 만화같은 이미지로 변경합니다.
  - 매개변수
    + img: imread or read함수의 결과 (이미지 데이터)
  - 반환값
    + ret: cartoonize 변환 이미지


## cFace 클래스

+ 기능
  - 얼굴을 탐색합니다.
  - 얼굴을 학습/저장/삭제합니다.
  - 학습된 얼굴을 인식합니다.
  - 얼굴로 나이/성별은 추정합니다.

+ cFace.__init__(model_path, data_path)
  - 기능: cFace 클래스를 초기화합니다.
    + facedb 생성
    + 얼굴인식/분석/탐지에 대한 모델 로드
  - 매개변수
    + model_path: model파일의 경로를 설정합니다.
    + data_path: data파일의 경로를 설정합니다.

+ cFace.get_db()
  - 기능: 사용 중인 얼굴 데이터베이스를 확인합니다.
  - 반환값
    + ret: 현재 로드된 얼굴 데이터베이스

+ cFace.init_db()
  - 기능: 얼굴 데이터베이스를 초기화합니다.

+ cFace.load_db(filename)
  - 기능: 얼굴 데이터베이스 파일을 불러옵니다.
  - 매개변수
    + filename: 불러올 데이터베이스 파일이름

+ cFace.save_db(filename)
  - 기능: 얼굴 데이터베이스를 파일로 저장합니다.
  - 매개변수
    + filename: 저장할 데이터베이스 파일이름

+ cFace.train_face(img, face, name)
  - 기능: 얼굴을 학습합니다.
  - 매개변수
    + img: 학습할 이미지 데이터 (imread or read함수로 반환받은 데이터)
    + face: 얼굴 1개 위치 (cFace.detect()함수의 결과값 중 1개)
    + name: 학습할 얼굴 이름

+ cFace.delete_face(name)
  - 기능: 등록된 얼굴을 삭제합니다.
  - 매개변수
    + name: 삭제할 얼굴 이름
  - 반환값
    + ret: 성공/실패

+ cFace.recognize(img, face)
  - 기능: 등록된 얼굴을 인식합니다.
  - 매개변수
    + img: 인식할 얼굴이 있는 이미지 데이터(imread or read함수의 결과)
    + face: 얼굴 1개 위치 (cFace.detect()함수의 결과값 중 1개)

  - 반환값
    + ret: {"name":이름, "score":정확도} - (정확도 0.4 이하 동일인 판정) or False

+ cFace.detect(img)
  - 기능: 얼굴을 탐색합니다.
  - 매개변수
    + img: 이미지 데이터(imread or read함수로 반환받은 데이터)
  - 반환값
    + ret: 인식된 얼굴들의 (x,y,w,h) 배열

+ cFace.get_ageGender(img, face)
  - 기능: 얼굴의 나이, 성별을 추정합니다.
  - 매개변수
    + img: 이미지 데이터(imread or read함수로 반환받은 데이터)
    + face: 얼굴 1개 위치 (cFace.detect()함수의 결과값 중 1개)
  - 반환값
    + ret: {"age":나이, "gender":성별}

### 참고: https://github.com/kairess/age_gender_estimation


## cDetect 클래스

+ 기능
  - 20개 class 안에서의 객체 인식
  - QR/바코드 인식
  - 문자 인식(OCR, Tesseract)

+ cDetect.__init__(model_path)
  - 기능: cDetect 클래스를 초기화합니다.
  - 매개변수
    + model_path: model파일의 경로를 설정합니다.

+ cDetect.detect_object(img)
  - 기능: 이미지 안의 객체를 인식합니다. (20개 클래스의 사물인식)
  - 인식가능한 사물
    ["background", "aeroplane", "bicycle", "bird", "boat",
     "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
     "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
     "sofa", "train", "tvmonitor"]
  - 매개변수
    + img: 이미지 데이터(imread or read함수로 반환받은 데이터)
  - 반환값
    + ret: {"name":이름, "score":점수, "position":사물좌표(startX, startY, endX, endY)}

+ cDetect.detect_qr(img)
  - 기능: 이미지 안의 QR코드 및 바코드를 인식합니다.
  - 매개변수
    + img: 이미지 데이터(imread or read함수로 반환받은 데이터)
  - 반환값
    + ret: {"type":바코드/QR코드, "data":내용}

+ cDetect.detect_text(img)
  - 기능: 이미지 안의 문자를 인식합니다.
  - 매개변수
    + img: 이미지 데이터(imread or read함수로 반환받은 데이터)
  - 반환값
    + ret: 인식된 문자열
