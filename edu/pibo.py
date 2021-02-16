import os, sys, time
# sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
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

onair = False

class Edu_Pibo:
    def __init__(self):
        self.audio = cAudio()
        self.oled = cOled(conf=cfg)
        self.speech = cSpeech(conf=cfg)
        self.dialog = cDialog(conf=cfg)
        self.device = cDevice()
        self.motion = cMotion(conf=cfg)
        self.camera = cCamera()
        self.face = cFace(conf=cfg)
        self.detect = cDetect(conf=cfg)


    def play(self, filename, out='local', volume='-2000'):
        self.audio.play(filename, out, volume)


    def stop(self):
        self.audio.stop()


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

        if len(color) == 3:
            self.device.send_raw(f"#20:{color}!")
        elif len(color) == 6:
            self.device.send_raw(f"#23:{color}!")
        elif len(color) == 1:
            color = color_list[color[-1].lower()]
            self.device.send_raw(f"#20:{color}!")


    def eye_off(self):
        self.device.send_raw("#20:0,0,0:!")


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
            print(ans)
        else:
            if system == "PIR":
                self.device.send_cmd(device_list[system], "on")
            else:
                self.device.send_cmd(device_list[system])
            ret = self.device.send_cmd(device_list["SYSTEM"])
            ans = system + ': ' + ret[3:]
            print(ans)


    def motor(self, n, position, speed=None, accel=None):
        self.motion.set_speed(n, speed)
        self.motion.set_acceleration(n, accel)
        self.motion.set_motor(n, position)


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


    def motors_movetime(self, positions, movetime=None):
        self.motion.set_motors(positions, movetime)


    def get_motion(self, name=None):
        self.motion.get_motion(name)


    def set_motion(self, name, cycle):
        self.motion.set_motion(name, cycle)


    def draw_text(self, points, text, size=None):
        self.oled.set_font(size=size)
        self.oled.draw_text(points, text)


    def draw_image(self, filename):
        self.oled.draw_image(filename)


    def draw_figure(self, points, shape, fill=None):
        if shape in ('rectangle', '네모', '사각형'):
            self.oled.draw_rectangle(points, fill)
        elif shape in ('circle', '원', '동그라미','타원'):
            self.oled.draw_ellipse(points, fill)
        elif shape in ('line', '선', '직선'):
            self.oled.draw_line(points)
        else:
            self.draw_text((8,20), '다시 입력해주세요', 15)


    def invert(self):
        self.oled.invert()


    def show_display(self):
        self.oled.show()


    def clear_display(self):
        self.oled.clear()


    def translate(self, string, to='ko'):
        return self.speech.translate(string, to)


    def tts(self, string, filename='tts.mp3', voice='MAN_READ_CALM', lang='ko'):
        self.speech.tts(string, filename, lang)


    def stt(self, filename='stream.wav', lang='ko-KR', timeout=5):
        self.speech.stt(filename, lang, timeout)


    def conversation(self, q):
        return self.dialog.get_dialog(q)


    def onair(self):
        vs = VideoStream(width=128, height=64).start()

        while True:
            if onair == False:
                vs.stop()
                self.oled.clear()
                break
            img = vs.read()
            self.oled.draw_streaming(img)
            self.oled.show()
            self.camera.waitKey(1)


    def start_camera(self):
        global onair

        if onair:
            return
        onair = True
        t = Thread(target=self.onair, args=())
        t.start()


    def stop_camera(self):
        global onair

        onair = False


    def capture(self, filename="capture.png"):
        global onair

        if onair:
            self.stop_camera()
            capture_img = self.camera.read(w=128, h=64)
            self.camera.imwrite(filename, capture_img)
            self.oled.clear()
            self.oled.draw_image(filename)
            self.oled.show()
            return
        else:
            self.send_msg()


    def search_object(self):
        global onair
        
        if onair:
            img = self.camera_read()
            return self.detect.detect_object(img)
        else:
            self.send_msg()


    def search_qr(self):
        global onair

        if onair:
            img = self.camera_read()
            return self.detect.detect_qr(img)
        else:
            self.send_msg()


    def search_text(self):
        global onair

        if onair:
            img = self.camera_read()
            return self.detect.detect_text(img)
        else:
            self.send_msg()


    def search_color(self):
        global onair
        
        if onair:
            img = self.camera_read()
            # 색깔 구별 메서드 구현
            # return self.detect.detect_text(img)
        else:
            self.send_msg()


    def search_face(self):
        global onair

        if onair:
            img = self.camera_read()
            faceList = self.face.detect(img)
            self.camera.imwrite('face.png', img)

            if len(faceList) < 1:
                print("No Face")
                return

            ret = self.face.get_ageGender(img, faceList[0])
            age = ret["age"]
            gender = ret["gender"]

            x,y,w,h = faceList[0]  
            self.camera.rectangle(img, (x,y), (x+w, y+h))

            ret = self.face.recognize(img, faceList[0])
            name = "Guest" if ret == False else ret["name"]
            result = self.camera.putText(img, "{}/ {} {}".format(name, gender, age), (x-10, y-10), size=0.5)
            self.camera.imwrite('face.png', result)

            return {"name": name, "gender": gender, "age": age}
        else:
            self.send_msg()


    def train_face(self, name):
        global onair

        if onair:
            img = self.camera_read()
            faces = self.face.detect(img)

            if len(faces) < 1:
                print(" No Face")
            else:
                self.face.train_face(img, faces[0], name)
                self.face.save_db("./facedb")
                print(" Train:", self.face.get_db()[0])
        else:
            send_msg()


    def delete_face(self, name):
        ret = self.face.delete_face(name)
        return ret


    def train_myObject(self, name):
        global onair

        if onair:
            img = self.camera_read()
            objects = self.detect.detect_object(img)

            if len(objects) < 1:
                print("No Object")
            # else:

        else:
            send_msg()


    def camera_read(self):
        self.stop_camera()
        img = self.camera.read()
        return img


    def send_msg(self):
        self.draw_text((11, 18), "카메라를 켜주세요.", 15)
        self.oled.show()
