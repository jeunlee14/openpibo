import os, sys, time, cv2

from utils.config import Config as cfg
sys.path.append(cfg.OPENPIBO_PATH + '/lib')

from audio.audiolib import cAudio
from oled.oledlib import cOled
from speech.speechlib import cSpeech
from speech.speechlib import cDialog
from device.devicelib import cDevice
from motion.motionlib import cMotion
from vision.visionlib import cCamera
from vision.visionlib import cFace
from vision.visionlib import cDetect
from vision.stream import VideoStream

from threading import Thread


class Edu_Pibo:
    def __init__(self):
        self.ret = True
        self.onair = False
        self.img = ""
        self.audio = cAudio()
        self.oled = cOled(conf=cfg)
        self.speech = cSpeech(conf=cfg)
        self.dialog = cDialog(conf=cfg)
        self.device = cDevice()
        self.motion = cMotion(conf=cfg)
        self.camera = cCamera()
        self.face = cFace(conf=cfg)
        self.detect = cDetect(conf=cfg)


    # [Audio] - mp3/wav 파일 재생
    def play(self, filename, out='local', volume='-2000'):
        self.audio.play(filename, out, volume)
        return self.ret, None


    # [Audio] - 오디오 재생 정지
    def stop(self):
        self.audio.stop()
        return self.ret, None


    # [Neopixel] - LED ON
    def eye_on(self, *color):
        color_list = {
            'black': (0,0,0),
            'white': (255,255,255),
            'red': (255,0,0),
            'orange': (200,75,0),
            'yellow': (255,255,0),
            'green': (0,255,0),
            'blue': (0,0,255),
            'aqua': (0,255,255),
            'purple': (255,0,255),    
            'pink': (255,51,153),
        }   
        
        # 양쪽 눈 제어(RGB)
        if len(color) == 3:
            self.device.send_raw(f"#20:{color}!")
        # 양쪽 눈 개별 제어(RGB)
        elif len(color) == 6:
            self.device.send_raw(f"#23:{color}!")
        # 양쪽 눈 제어(string)
        elif len(color) == 1:
            color = color_list[color[-1].lower()]
            self.device.send_raw(f"#20:{color}!")
        else:
            return False, None

        return self.ret, None


    # [Neopixel] - LED OFF
    def eye_off(self):
        self.device.send_raw("#20:0,0,0:!")
        return self.ret, None


    # [Device] - 부품 상태 확인
    def check_device(self, system):
        device_list = {
            "BUTTON":"13",
            "DC":"14",
            "BATTERY":"15",
            "PIR":"30",
            "TOUCH":"31",
            "SYSTEM":"40",
        }
        system = system.upper()

        if system in  ( "BUTTON", "BATTERY", "DC"):
            ret = self.device.send_cmd(device_list[system])
            ans = system + ': ' + ret[3:]

            return self.ret, ans
        else:
            if system == "PIR":
                self.device.send_cmd(device_list[system], "on")
            else:
                self.device.send_cmd(device_list[system])
            ret = self.device.send_cmd(device_list["SYSTEM"])
            ans = system + ': ' + ret[3:]

            return self.ret, ans


    # [Motion] - 모터 1개 제어(위치/속도/가속도)
    def motor(self, n, position, speed=None, accel=None):
        if n < 0 or n > 9:
            return False, "Error > Channel value should be 0-9"
        elif speed is not None and (speed < 0 or speed > 255):
            return False, "Error > Speed value should be 0-255"
        elif accel is not None and (speed < 0 or speed > 255):
            return False, "Error > Acceleration value should be 0-255"

        self.motion.set_speed(n, speed)
        self.motion.set_acceleration(n, accel)
        self.motion.set_motor(n, position)

        return self.ret, None


    # [Motion] - 모든 모터 제어(위치/속도/가속도)
    def motors(self, positions, speed=None, accel=None):
        mpos = [positions[i]*10 for i in range(len(positions))]

        if speed == None and accel == None:
            os.system("servo mwrite {}".format(" ".join(map(str, mpos))))
        if speed:
            os.system("servo speed all {}".format(" ".join(map(str, speed))))
            os.system("servo mwrite {}".format(" ".join(map(str, mpos))))
        if accel:
            os.system("servo accelerate all {}".format(" ".join(map(str, accel))))
            os.system("servo mwrite {}".format(" ".join(map(str, mpos))))

        return self.ret, None


    # [Motion] - 모든 모터 제어(movetime)
    def motors_movetime(self, positions, movetime=None):
        self.motion.set_motors(positions, movetime)
        return self.ret, None


    # [Motion] - 모션 종류 또는 모션 상세 정보 조회
    def get_motion(self, name=None):
        ret = self.motion.get_motion(name)
        return self.ret, ret


    # [Motion] - 모션 수행
    def set_motion(self, name, cycle):
        ret = self.motion.set_motion(name, cycle)
        if ret ==  False:
            return ret, "Profile not exist " + name 
        return ret, None


    # [OLED] - 문자
    def draw_text(self, points, text, size=None):
        self.oled.set_font(size=size)
        self.oled.draw_text(points, text)
        return self.ret, None


    # [OLED] - 이미지
    def draw_image(self, filename):
        size_check = cv2.imread(filename).shape
        if size_check[0] != 64 or size_check[1] != 128:
            return False, "128X64 파일만 가능합니다."

        self.oled.draw_image(filename)
        return self.ret, None


    # [OLED] - 도형
    def draw_figure(self, points, shape, fill=None):
        if shape in ('rectangle', '네모', '사각형'):
            self.oled.draw_rectangle(points, fill)
        elif shape in ('circle', '원', '동그라미','타원'):
            self.oled.draw_ellipse(points, fill)
        elif shape in ('line', '선', '직선'):
            self.oled.draw_line(points)
        else:
            self.draw_text((8,20), '다시 입력해주세요', 15)
            return False, None
        return self.ret, None


    # [OLED] - 반전
    def invert(self):
        self.oled.invert()
        return self.ret, None


    # [OLED] - 화면 출력
    def show_display(self):
        self.oled.show()
        return self.ret, None


    # [OLED] - 화면 지움
    def clear_display(self):
        self.oled.clear()
        return self.ret, None


    # [Speech] - 문장 번역
    def translate(self, string, to='ko'):
        ret = self.speech.translate(string, to)
        return self.ret, ret


    # [Speech] - TTS
    def tts(self, string, filename='tts.mp3', lang='ko'):
        if '<speak>' and '</speak>' not in string:
            return False, None

        self.speech.tts(string, filename, lang)
        return self.ret, None


    # [Speech] - STT
    def stt(self, filename='stream.wav', lang='ko-KR', timeout=5):
        self.speech.stt(filename, lang, timeout)
        return self.ret, None


    # [Speech] - 대화
    def conversation(self, q):
        ret = self.dialog.get_dialog(q)
        return self.ret, ret


    # [Vision] - start_camera thread
    def camera_on(self):
        vs = VideoStream(width=128, height=64).start()

        while True:
            if self.onair == False:
                vs.stop()
                self.oled.clear()
                break
            self.img = vs.read()
            self.oled.draw_streaming(self.img)
            self.oled.show()


    # [Vision] - 카메라 ON
    def start_camera(self):
        if self.onair:
            return

        self.onair = True
        t = Thread(target=self.camera_on, args=())
        t.start()
        return self.ret, None


    # [Vision] - 카메라 OFF
    def stop_camera(self):
        if self.onair == False:
            return False, None

        self.onair = False
        return self.ret, None


    # [Vision] - 사진 촬영
    def capture(self, filename="capture.png"):
        if self.onair:
            self.camera.imwrite(filename, self.img)
        else:
            img = self.camera.read(w=128, h=64)
            self.camera.imwrite(filename, img)
            self.oled.draw_image(filename)
            self.oled.show()
        return self.ret, None


    # [Vision] - 객체 인식
    def search_object(self):
        if self.onair:
            img = self.img
        else:
            img = self.camera.read()
        ret = self.detect.detect_object(img)
        return self.ret, ret


    # [Vision] - QR/바코드 인식
    def search_qr(self):
        if self.onair:
            ret = self.detect.detect_qr(self.img)
            return self.ret, ret
        else:
            img = self.camera.read()
            ret = self.detect.detect_qr(img)
            return self.ret, ret


    # [Vision] - 문자 인식
    def search_text(self):
        if self.onair:
            ret = self.detect.detect_text(self.img)
            return self.ret, ret
        else:
            img = self.camera.read()
            ret = self.detect.detect_text(img)
            return self.ret, ret


    # [Vision] - 컬러 인식
    # def search_color(self):
    #     if self.onair:
    #         img = self.camera_read()
            # ret = self.detect.detect_color(img)
            # return ret
        # else:
        #     pass


    # [Vision] - 얼굴 인식
    def search_face(self, filename="face.png"):
        if self.onair:
            img = self.img
        else:
            img = self.camera.read()

        faceList = self.face.detect(img)
        if len(faceList) < 1:
            return False, "No Face"

        ret = self.face.get_ageGender(img, faceList[0])
        age = ret["age"]
        gender = ret["gender"]

        x,y,w,h = faceList[0]  
        self.camera.rectangle(img, (x,y), (x+w, y+h))

        ret = self.face.recognize(img, faceList[0])
        name = "Guest" if ret == False else ret["name"]
        score = 0 if ret == False else ret["score"]
        result = self.camera.putText(img, "{}/ {} {}".format(name, gender, age), (x-10, y-10), size=0.5)
        # self.camera.imwrite(filename, result)

        return self.ret, {"name": name, "score": score, "gender": gender, "age": age}


    # [Vision] - 얼굴 학습
    def train_face(self, name):
        if self.onair:
            img = self.img
        else:
            img = self.camera.read()
    
        faces = self.face.detect(img)
        if len(faces) < 1:
            return False, "No Face"
        else:
            self.face.train_face(img, faces[0], name)
            return True, None


    # [Vision] - 사용 중인 facedb 확인
    def get_facedb(self):
        facedb = self.face.get_db()
        return self.ret, facedb


    # [Vision] - facedb 초기화
    def init_facedb(self):
        self.face.init_db()
        return self.ret, None


    # [Vision] - facedb 불러옴
    def load_facedb(self, filename):
        self.face.load_db(filename)
        return self.ret, None


    # [Vision] - facedb를 파일로 저장
    def save_facedb(self, filename):
        self.face.save_db(filename)
        return self.ret, None


    # [Vision] - facedb에 등록된 얼굴 삭제
    def delete_face(self, name):
        ret = self.face.delete_face(name)
        return ret, None
        

    # [Vision] - 객체 학습
    # def train_myObject(self, name):
    #    pass