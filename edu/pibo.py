import os, sys, time, cv2
import numpy as np

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
        self.onair = False
        self.img = ""
        self.check = False
        self.flash = False
        self.audio = cAudio()
        self.oled = cOled(conf=cfg)
        self.speech = cSpeech(conf=cfg)
        self.dialog = cDialog(conf=cfg)
        self.device = cDevice()
        self.motion = cMotion(conf=cfg)
        self.camera = cCamera()
        self.face = cFace(conf=cfg)
        self.detect = cDetect(conf=cfg)
        self.device.send_cmd(self.device.code['PIR'], "on")


    # [Audio] - mp3/wav 파일 재생
    def play_audio(self, filename=None, out='local', volume='-2000', background=True):
        if filename is not None:
            ext = filename.find('.')
            file_ext = filename[ext+1:]
            if file_ext != ('mp3' or 'wav'):
                return False, "Error > Audio filename must be 'mp3', 'wav'" 
        try:
            if out not in ("local", "hdmi", "both"):
                return False, "Error > Output device must be 'local', 'hdmi', 'both'"
            self.audio.play(filename, out, volume, background)
            return True, None
        except Exception as e:
            return False, e


    # [Audio] - 오디오 재생 정지
    def stop_audio(self):
        try:
            self.audio.stop()
            return True, None
        except Exception as e:
            return False, e


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
  
        if len(color) == 0:
            return False, "Error > RGB or Color is required"
        try:
            if str(color[-1]).isdigit():
                for i in color:
                    if i < 0 or i > 255:
                        return False, "Error > RGB value should be 0~255"
                    else:
                        if len(color) == 3:
                            self.device.send_raw("#20:{}!".format(",".join(str(p) for p in color)))
                        elif len(color) == 6:
                            self.device.send_raw("#23:{}!".format(",".join(str(p) for p in color)))
                        else:
                            return False, "Error > Invalid format"
            else:
                color = color[-1].lower()
                if color not in color_list.keys():
                    return False, "Error > The color does not exist"
                else:
                    color = color_list[color]
                    self.device.send_raw("#20:{}!".format(",".join(str(p) for p in color)))
            return True, None
        except Exception as e:
            return False, e


    # [Neopixel] - LED OFF
    def eye_off(self):
        try:
            self.device.send_raw("#20:0,0,0:!")
            return True, None
        except Exception as e:
            return False, e


    # [Device] - 디바이스 상태 확인
    def check_device(self, system):
        system = system.upper()
        try:
            if system == "BATTERY":
                ret = self.device.send_cmd(self.device.code[system])
                ans = system + ': ' + ret[3:]
            elif system == "SYSTEM":
                ret = self.device.send_cmd(self.device.code["SYSTEM"])

                sys = ""
                result = []
                for i in ret[3:]:
                    if i == "-":
                        result.append(sys)
                        sys = ""
                        continue
                    sys += i

                system_dict = {"PIR": "", "TOUCH": "", "DC_CONN": "", "BUTTON": "",}
                system_dict["PIR"] = result[0]
                system_dict["TOUCH"] = result[1]
                system_dict["DC_CONN"] = result[2]
                system_dict["BUTTON"] = result[3]
                ans = system_dict
            return True, ans
        except UnboundLocalError:
            return False, "Error > System must be 'battery', 'system'"
        except Exception as e:
            return False, e


    # [Device] - start_devices thread
    def thread_device(self, func):
        self.system_check_time = time.time()
        self.battery_check_time = time.time()

        while True:
            if self.check == False:
                return

            if time.time() - self.system_check_time > 1:
                ret = self.device.send_cmd(self.device.code["SYSTEM"])
                msg = "SYSTEM" + ': ' + ret[3:]
                func(msg)
                self.system_check_time = time.time()
            
            if time.time() - self.battery_check_time > 10:
                ret = self.device.send_cmd(self.device.code["BATTERY"])
                msg = "BATTERY" + ': ' + ret[3:]
                func(msg)
                self.battery_check_time = time.time()

            time.sleep(0.1)


    # [Device] - 디바이스 상태 확인(thread)
    def start_devices(self, func):
        try:
            self.check = True
            t = Thread(target=self.thread_device, args=(func,))
            t.daemon = True
            t.start()
            return True, None
        except Exception as e:
            return False, e


    # [Device] - 디바이스 상태 확인 종료
    def stop_devices(self):
        try:
            self.check = False
            return True, None
        except Exception as e:
            return False, e


    # [Motion] - 모터 1개 제어(위치/속도/가속도)
    def motor(self, n, position, speed=None, accel=None):
        if n < 0 or n > 9:
            return False, "Error > Channel value should be 0~9"
        if position > 80 or position < -80:
            return False, "Error > Position value should be -80~80"
        if speed is not None and (speed < 0 or speed > 255):
            return False, "Error > Speed value should be 0~255"
        if accel is not None and (accel < 0 or accel > 255):
            return False, "Error > Acceleration value should be 0~255"

        try:
            self.motion.set_speed(n, speed)
            self.motion.set_acceleration(n, accel)
            self.motion.set_motor(n, position)
            return True, None

        except Exception as e:
            return False, e


    # [Motion] - 모든 모터 제어(위치/속도/가속도)
    def motors(self, positions, speed=None, accel=None):
        if len(positions) != 10:
            return False, "Error > 10 positions are required"
        if speed is not None and len(speed) != 10:
            return False, "Error > 10 speeds are required"
        if accel is not None and len(accel) != 10:
            return False, "Error > 10 accelerations are require"

        try:
            mpos = [positions[i]*10 for i in range(len(positions))]

            if speed is None and accel is None:
                os.system("servo mwrite {}".format(" ".join(map(str, mpos))))
            elif speed is not None and accel is None:
                os.system("servo speed all {}".format(" ".join(map(str, speed))))
                os.system("servo mwrite {}".format(" ".join(map(str, mpos))))
            elif accel is not None and speed is None:
                os.system("servo accelerate all {}".format(" ".join(map(str, accel))))
                os.system("servo mwrite {}".format(" ".join(map(str, mpos))))
            elif speed is not None and accel is not None:
                os.system("servo speed all {}".format(" ".join(map(str, speed))))
                os.system("servo accelerate all {}".format(" ".join(map(str, accel))))
                os.system("servo mwrite {}".format(" ".join(map(str, mpos))))
            return True, None
        except Exception as e:
            return False, e


    # [Motion] - 모든 모터 제어(movetime)
    def motors_movetime(self, positions, movetime=None):
        if len(positions) != 10:
            return False, "Error > 10 positions are required"
        elif type(movetime) != int:
            return False, "Error > Movetime is only available int type"

        try:
            self.motion.set_motors(positions, movetime)
            return True, None
        except Exception as e:
            return False, e


    # [Motion] - 모션 종류 또는 모션 상세 정보 조회
    def get_motion(self, name=None):
        try:
            ret = self.motion.get_motion(name)
            return True, ret
        except Exception as e:
            return False, e


    # [Motion] - 모션 수행
    def set_motion(self, name, cycle=1):
        try:
            ret = self.motion.set_motion(name, cycle)
            if ret ==  False:
                return ret, "Error > " + name + " not exist in the profile" 
            return ret, None
        except Exception as e:
            return False, e


    # [OLED] - 문자
    def draw_text(self, points, text, size=None):
        if type(points) != tuple:
            return False, "Error > Invalid format"
        else:
            if len(points) != 2:
                return False, "Error > 2 points are required"

        try:
            self.oled.set_font(size=size)
            self.oled.draw_text(points, text)
            return True, None
        except IndexError as e:
            return False, e
        except TypeError as e:
            return False, e
        except Exception as e:
            return False, e


    # [OLED] - 이미지
    def draw_image(self, filename=None):
        try:
            self.oled.draw_image(filename)
            return True, None
        except Exception as e:
            return False, e


    # [OLED] - 도형
    def draw_figure(self, points, shape, fill=None):
        try:
            if shape == 'rectangle' or shape == '사각형' or shape == '네모':
                self.oled.draw_rectangle(points, fill)
            elif shape == 'circle' or shape == '원' or shape == '동그라미' or shape == '타원':
                self.oled.draw_ellipse(points, fill)
            elif shape == 'line' or shape == '선' or shape == '직선':
                self.oled.draw_line(points)
            else:
                return False, "Error > The shape does not exist"
            return True, None
        except Exception as e:
            return False, e


    # [OLED] - 반전
    def invert(self):
        try:
            self.oled.invert()
            return True, None
        except Exception as e:
            return False, e


    # [OLED] - 화면 출력
    def show_display(self):
        try:
            self.oled.show()
            return True, None
        except Exception as e:
            return False, e


    # [OLED] - 화면 지움
    def clear_display(self):
        try:
            self.oled.clear()
            return True, None
        except Exception as e:
            return False, e


    # [Speech] - 문장 번역
    def translate(self, string=None, to='ko'):
        if string is None:
            return False, "translate() missing 1 required positional argument: 'string'"
        try:
            ret = self.speech.translate(string, to)
            return True, ret
        except Exception as e:
            return False, e


    # [Speech] - TTS
    def tts(self, string, filename='tts.mp3', lang='ko'):
        voice_list= ('WOMAN_READ_CALM' or 'MAN_READ_CALM' or 'WOMAN_DIALOG_BRIGHT' or 'MAN_DIALOG_BRIGHT')

        if '<speak>' not in string or '</speak>' not in string:
            return False, "Error > Invalid string format"
        elif '<voice' in string and '</voice>' in string:
            voice_start = string.find('=')
            voice_end = string.find('>', voice_start)
            voice_name = string[voice_start+2:voice_end-1]
            if voice_name not in voice_list:
                return False, "Error > The voice name does not exist" 

        try:
            self.speech.tts(string, filename, lang)
            return True, None
        except Exception as e:
            return False, e


    # [Speech] - STT
    def stt(self, filename='stream.wav', lang='ko-KR', timeout=5):
        try:
            ret = self.speech.stt(filename, lang, timeout)
            return True, ret
        except Exception as e:
            return False, e


    # [Speech] - 대화
    def conversation(self, q):
        try:
            ret = self.dialog.get_dialog(q)
            return True, ret
        except Exception as e:
            return False, e


    # [Vision] - start_camera thread
    def camera_on(self):
        vs = VideoStream().start()

        while True:
            if self.onair == False:
                vs.stop()
                break
            self.img = vs.read()
            img = self.img
            img = cv2.resize(img, (128,64))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            #_, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
            if self.flash:
                rows, cols = img.shape[0:2]
                m45 = cv2.getRotationMatrix2D((cols/2,rows/2), 45, 0.8)
                img = cv2.warpAffine(img, m45, (cols,rows))
                self.oled.nparray_to_PIL(img)
                self.oled.show()
                time.sleep(0.3)
                self.flash = False
                continue
            self.oled.nparray_to_PIL(img)
            self.oled.show()


    # [Vision] - 카메라 ON
    def start_camera(self):
        try:
            if self.onair:
                return
            self.onair = True
            t = Thread(target=self.camera_on, args=())
            # t.daemon = True
            t.start()
            return True, None
        except Exception as e:
            return False, e


    # [Vision] - 카메라 OFF
    def stop_camera(self):
        try:
            if self.onair == False:
                return False, None
            self.onair = False
            time.sleep(0.5)
            return True, None
        except Exception as e:
            return False, e


    # [Vision] - 사진 촬영
    def capture(self, filename="capture.png"):
        try:
            if self.onair:
                self.camera.imwrite(filename, self.img)
                self.flash = True
            else:
                img = self.camera.read()
                self.camera.imwrite(filename, img)
                img = cv2.resize(img, (128,64))
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                #_, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
                self.oled.nparray_to_PIL(img)
                self.oled.show()
            return True, None
        except Exception as e:
            return False, e


    # [Vision] - 객체 인식
    def search_object(self):
        try:
            if self.onair:
                img = self.img
            else:
                img = self.camera.read()
            ret = self.detect.detect_object(img)
            return True, ret
        except Exception as e:
            return False, e


    # [Vision] - QR/바코드 인식
    def search_qr(self):
        try:
            if self.onair:
                img = self.img
            else:
                img = self.camera.read()
            ret = self.detect.detect_qr(img)
            return True, ret
        except Exception as e:
            return False, e


    # [Vision] - 문자 인식
    def search_text(self):
        try:
            if self.onair:
                img = self.img
            else:
                img = self.camera.read()
            ret = self.detect.detect_text(img)
            return True, ret
        except Exception as e:
            return False, e
        

    # [Vision] - 컬러 인식
    def search_color(self):
        try:
            if self.onair:
                img = self.img
            else:
                img = self.camera.read()

            height, width = img.shape[:2]
            img_hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
            cnt = 0
            sum_hue = 0
            
            # 평균 패치 측정(j: Height, i: width)
            for i in range(50, width-50, 20):
                for j in range(50, height-50, 20):
                    sum_hue += (img_hls[j, i, 0]*2)
                    cnt += 1
            
            hue = round(sum_hue/cnt)

            if ( 0 <= hue <= 30) or (330 <=  hue <= 360):
                return True, "Red"
            elif (31 <=  hue <= 59):
                return True, "Orange"
            elif (60 <=  hue <= 85):
                return True, "Yellow"
            elif (86 <=  hue <= 159):
                return True, "Green"
            elif (160 <=  hue <= 209):
                return True, "Skyblue"
            elif (210 <=  hue <= 270):
                return True, "Blue"
            elif (271 <=  hue <= 290):
                return True, "Purple"
            elif (291<=  hue <= 329):
                return True, "Magenta"
            else:
                return False, "Error > Can't check color"
        except Exception as e:
            return False, e


    # [Vision] - 얼굴 탐색
    def detect_face(self):
        try:
            if self.onair:
                img = self.img
            else:
                img = self.camera.read()
            faceList = self.face.detect(img)
            if len(faceList) < 1:
                return False, "No Face"
            return True, faceList
        except Exception as e:
            return False, e


    # [Vision] - 얼굴 인식
    def search_face(self, filename="face.png"):
        try:
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
            score = "-" if ret == False else ret["score"]
            result = self.camera.putText(img, "{}/ {} {}".format(name, gender, age), (x-10, y-10), size=0.5)
            self.camera.imwrite(filename, result)

            return True, {"name": name, "score": score, "gender": gender, "age": age}
        except Exception as e:
            return False, e


    # [Vision] - 얼굴 학습
    def train_face(self, name):
        try:
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
        except Exception as e:
            return False, e


    # [Vision] - 사용 중인 facedb 확인
    def get_facedb(self):
        try:
            facedb = self.face.get_db()
            return True, facedb
        except Exception as e:
            return False, e


    # [Vision] - facedb 초기화
    def init_facedb(self):
        try:
            self.face.init_db()
            return True, None
        except Exception as e:
            return False, e


    # [Vision] - facedb 불러옴
    def load_facedb(self, filename):
        try:
            self.face.load_db(filename)
            return True, None
        except Exception as e:
            return False, e


    # [Vision] - facedb를 파일로 저장
    def save_facedb(self, filename):
        try:
            self.face.save_db(filename)
            return True, None
        except Exception as e:
            return False, e


    # [Vision] - facedb에 등록된 얼굴 삭제
    def delete_face(self, name):
        try:
            ret = self.face.delete_face(name)
            return ret, None
        except Exception as e:
            return False, e