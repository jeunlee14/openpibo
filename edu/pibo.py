import sys, time, pickle

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
from queue import Queue
from pathlib import Path


alpha_cnt = 0
code_list = {
    "Success": 0,
    "Argument error": -1,
    "Extension error": -2,
    "NotFound error": -3,
    "Exist error": -4,
    "Range error": -5,
    "Running error": -6,
    "Syntax error": -7,
    "Exception error": -8,
}

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
        self.que = Queue()
        self.colordb = {
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
        self.motor_range = [25,35,80,30,50,25,25,35,80,30]


    # [Audio] - Play mp3/wav files
    def play_audio(self, filename=None, out='local', volume='-2000', background=True):
        if filename != None:
            file_list = ('mp3', 'wav')
            ext = filename.rfind('.')
            file_ext = filename[ext+1:]
            if file_ext not in file_list:
                return self.return_msg(False, "Extension error", "Audio filename must be 'mp3', 'wav'", None)
            file_exist = self.check_file(filename)
            if file_exist == False:
                return self.return_msg(False, "NotFound error", "The filename does not exist", None)
        else:
            return self.return_msg(False, "Argument error", "Filename is required", None)   
        try:
            if out not in ("local", "hdmi", "both"):
                return self.return_msg(False, "NotFound error", "Output device must be 'local', 'hdmi', 'both'", None)
            self.audio.play(filename, out, volume, background)
            return self.return_msg(True, "Success", "Success", None)
        except Exception as e:
            return self.return_msg(False, "Exception error", e, None)


    # [Audio] - Stop audio
    def stop_audio(self):
        try:
            self.audio.stop()
            return self.return_msg(True, "Success", "Success", None)
        except Exception as e:
            return self.return_msg(False, "Exception error", e, None)


    # [Neopixel] - Determine number or letter    
    def isAlpha(self, *value):
        global alpha_cnt

        if len(value) == 1 and type(*value) == str:
            return True
        else:
            for i in value:
                if str(i).isalpha():
                    alpha_cnt += 1
            if alpha_cnt == 0:
                return False
            return True


    # [Neopixel] - LED ON
    def eye_on(self, *color):
        if len(color) == 0:
            return self.return_msg(False, "Argument error", "RGB or Color is required", None)
        try:
            if self.isAlpha(*color) == False:
                for i in color:
                    if i < 0 or i > 255:
                        return self.return_msg(False, "Range error", "RGB value should be 0~255", None)
                if len(color) == 3:
                    cmd = "#20:{}!".format(",".join(str(p) for p in color))
                elif len(color) == 6:
                    cmd = "#23:{}!".format(",".join(str(p) for p in color))
                else:
                    return self.return_msg(False, "Syntax error", "Only 3 or 6 values can be entered", None)
            else:
                if len(color) == 1:
                    color = color[-1].lower()
                    if color not in self.colordb.keys():
                        return self.return_msg(False, "NotFound error", "{} does not exist in the colordb".format(color), None)
                    else:
                        color = self.colordb[color]
                        cmd = "#20:{}!".format(",".join(str(p) for p in color))
                elif len(color) == 2:
                    l_color, r_color = color[0].lower(), color[1].lower()
                    if l_color in self.colordb.keys() and r_color in self.colordb.keys():
                        l_color = self.colordb[l_color]
                        r_color = self.colordb[r_color]
                        color = l_color + r_color
                        cmd = "#23:{}!".format(",".join(str(p) for p in color))
                    else:
                        if l_color not in self.colordb.keys():
                            return self.return_msg(False, "NotFound error", "{} does not exist in the colordb".format(color[0]), None)
                        return self.return_msg(False, "NotFound error", "{} does not exist in the colordb".format(color[1]), None)
                else:
                    return self.return_msg(False, "Syntax error", "Only 2 colors can be entered", None)
            if self.check:
                self.que.put(cmd)
            else:
                self.device.send_raw(cmd)
            return self.return_msg(True, "Success", "Success", None)
        except Exception as e:
            return self.return_msg(False, "Exception error", e, None)


    # [Neopixel] - LED OFF
    def eye_off(self):
        try:
            cmd = "#20:0,0,0!"
            if self.check:
                self.que.put(cmd)
            else:
                self.device.send_raw(cmd)
            return self.return_msg(True, "Success", "Success", None)
        except Exception as e:
            return self.return_msg(False, "Exception error", e, None)


    # [Neopixel] - Create the color
    def add_color(self, color=None, *rgb):
        if color == None or type(color) != str:
            return self.return_msg(False, "Argument error", "Color is required", None)
        else:
            if not rgb:
                return self.return_msg(False, "Argument error", "RGB value is required", None)
            else:
                if len(rgb) != 3:
                    return self.return_msg(False, "Syntax error", "3 values are required(R,G,B)", None)
                for i in rgb:
                    if i < 0  or i > 255:
                        return self.return_msg(False, "Range error", "RGB value should be 0~255", None)
        try:
            color_list = self.get_colordb()["data"]
            if color in color_list.keys():
                return self.return_msg(False, "Exist error", "{} is already exist".format(color), None)
            color_list[color] = rgb
            return self.return_msg(True, "Success", "Success", None)
        except Exception as e:
            return self.return_msg(False, "Exception error", e, None)


    # [Neopixel] - Get colordb
    def get_colordb(self):
        try:
            return self.return_msg(True, "Success", "Success", self.colordb)
        except Exception as e:
            return self.return_msg(False, "Exception error", e, None)


    # [Neopixel] - Reset colordb
    def init_colordb(self):
        try:
            self.colordb = {
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
            return self.return_msg(True, "Success", "Success", None)
        except Exception as e:
            return self.return_msg(False, "Exception error", e, None)


    # [Neopixel] - Save the colordb as a file
    def save_colordb(self, filename=None):
        if filename == None:
            return self.return_msg(False, "Argument error", "Filename is required", None)
        try:
            with open(filename, "w+b") as f:
                pickle.dump(self.colordb, f)
            return self.return_msg(True, "Success", "Success", None)
        except Exception as e:
            return self.return_msg(False, "Exception error", e, None)


    # [Neopixel] - Load colordb
    def load_colordb(self, filename=None):
        if filename == None:
            return self.return_msg(False, "Argument error", "Filename is required", None)
        else:
            file_exist = self.check_file(filename)
            if file_exist == False:
                return self.return_msg(False, "NotFound error", "The filename does not exist", None)
        try:
            with open(filename, "rb") as f:
                self.colordb = pickle.load(f)
                return self.return_msg(True, "Success", "Success", None)
        except Exception as e:
            return self.return_msg(False, "Exception error", e, None)


    # [Neopixel] - Delete color in the colordb
    def delete_color(self, color=None):
        if color == None:
            return self.return_msg(False, "Argument error", "Color is required", None)
        try:
            ret = color in self.colordb.keys()
            if ret == True:
                del self.colordb[color]
                return self.return_msg(ret, "Success", "Success", None)
            return self.return_msg(False, "NotFound error", "{} not exist in the colordb".format(color), None)
        except Exception as e:
            return self.return_msg(False, "Exception error", e, None)


    # [Device] - Check device
    def check_device(self, system=None):
        device_list = ('BATTERY', 'SYSTEM')
        if system:
            system = system.upper()
            if system not in device_list:
                return self.return_msg(False, "NotFound error", "System must be 'battery', 'system'", None)
        else:
            return self.return_msg(False, "Argument error", "Enter the device name to check", None)
        try:
            ret = self.device.send_cmd(self.device.code[system])
            idx = ret.find(':')
            if system == "BATTERY":
                ans = system + ret[idx:]
            elif system == "SYSTEM":
                result = ret[idx+1:].split('-')
                ans = {"PIR": "", "TOUCH": "", "DC_CONN": "", "BUTTON": "",}
                ans["PIR"] = result[0]
                ans["TOUCH"] = result[1]
                ans["DC_CONN"] = result[2]
                ans["BUTTON"] = result[3]
            return self.return_msg(True, "Success", "Success", ans)
        except Exception as e:
            return self.return_msg(False, "Exception error", e, None)


    # [Device] - start_devices thread
    def thread_device(self, func):
        self.system_check_time = time.time()
        self.battery_check_time = time.time()
        while True:
            if self.check == False:
                break

            if self.que.qsize():
                self.device.send_raw(self.que.get())

            if time.time() - self.system_check_time > 1:
                ret = self.device.send_cmd(self.device.code["SYSTEM"])
                idx = ret.find(':')
                msg = "SYSTEM" + ret[idx:]
                func(msg)
                self.system_check_time = time.time()

            if time.time() - self.battery_check_time > 10:
                ret = self.device.send_cmd(self.device.code["BATTERY"])
                msg = "BATTERY" + ret[idx:]
                func(msg)
                self.battery_check_time = time.time()
            time.sleep(0.01)


    # [Device] - Check device(thread)
    def start_devices(self, func=None):
        if func == None:
            return self.return_msg(False, "Argument error", "Func is required", None)
        if self.check:
            return self.return_msg(False, "Running error", "start_devices() is already running", None)
        try:
            self.check = True
            t = Thread(target=self.thread_device, args=(func,))
            t.daemon = True
            t.start()
            return self.return_msg(True, "Success", "Success", None)
        except Exception as e:
            return self.return_msg(False, "Exception error", e, None)


    # [Device] - Stop check device
    def stop_devices(self):
        try:
            self.check = False
            return self.return_msg(True, "Success", "Success", None)
        except Exception as e:
            return self.return_msg(False, "Exception error", e, None)


    # [Motion] - Control 1 motor(position/speed/accel)
    def motor(self, n=None, position=None, speed=None, accel=None):
        if n != None:
            if n < 0 or n > 9:
                return self.return_msg(False, "Range error", "Channel value should be 0~9", None)
        else:
            return self.return_msg(False, "Argument error", "Channel is required", None)
        if position != None:
            if abs(position) > self.motor_range[n]:
                return self.return_msg(False, "Range error", "The position range of channel {} is -{} ~ {}".format(n, self.motor_range[n], self.motor_range[n]), None)
        else:
            return self.return_msg(False, "Argument error", "Position is required", None)
        try:
            if speed != None:
                if speed < 0 or speed > 255:
                    return self.return_msg(False, "Range error", "Speed value should be 0~255", None)
                self.motion.set_speed(n, speed)
            if accel != None:
                if accel < 0 or accel > 255:
                    return self.return_msg(False, "Range error", "Acceleration value should be 0~255", None)
                self.motion.set_acceleration(n, accel)
            self.motion.set_motor(n, position)
            return self.return_msg(True, "Success", "Success", None)
        except Exception as e:
            return self.return_msg(False, "Exception error", e, None)


    # [Motion] - Control all motors(position/speed/accel)
    def motors(self, positions=None, speed=None, accel=None):
        check = self.check_motor("position", positions)
        if check["result"] == False:
            return check
        try:
            if speed != None:
                check = self.check_motor("speed", speed)
                if check["result"] == False:
                    return check
                self.motion.set_speeds(speed)
            if accel != None:
                check = self.check_motor("acceleration", accel)
                if check["result"] == False:
                    return check
                self.motion.set_accelerations(accel)
            self.motion.set_motors(positions)
            return self.return_msg(True, "Success", "Success", None)
        except Exception as e:
            return self.return_msg(False, "Exception error", e, None)


    # [Motion] - Control all motors(movetime)
    def motors_movetime(self, positions=None, movetime=None):
        check = self.check_motor("position", positions)
        if check["result"] == False:
            return check
        if movetime and movetime < 0:
            return self.return_msg(False, "Range error", "Movetime is only available positive number", None)
        try:
            self.motion.set_motors(positions, movetime)
            return self.return_msg(True, "Success", "Success", None)
        except Exception as e:
            return self.return_msg(False, "Exception error", e, None)


    # [Motion] - Get motion type or motion details
    def get_motion(self, name=None):
        try:
            ret = self.motion.get_motion(name)
            return self.return_msg(True, "Success", "Success", ret)
        except Exception as e:
            return self.return_msg(False, "Exception error", e, None)


    # [Motion] - Set motion
    def set_motion(self, name=None, cycle=1):
        if name == None:
            return self.return_msg(False, "Argument error", "Name is required", None)
        try:
            ret = self.motion.set_motion(name, cycle)
            if ret ==  False:
                return self.return_msg(False, "NotFound error", "{} not exist in the motor profile".format(name), None)
            return self.return_msg(ret, "Success", "Success", None)
        except Exception as e:
            return self.return_msg(False, "Exception error", e, None)


    # [Motion] - Check motors array
    def check_motor(self, mode, values):
        try:
            if values == None or len(values) != 10:
                return self.return_msg(False, "Syntax error", "10 {}s are required".format(mode), None)
            if mode == "position":
                for i in range(len(values)):
                    if abs(values[i]) > self.motor_range[i]:
                        return self.return_msg(False, "Range error", "The position range of channel {} is -{} ~ {}".format(i, self.motor_range[i], self.motor_range[i]), None)
            else:
                for v in values:
                    if v < 0 or v > 255:
                        return self.return_msg(False, "Range error", "{} value should be 0~255".format(mode.capitalize()), None)
            return self.return_msg(True, "Success", "Success", None)
        except Exception as e: 
            return self.return_msg(False, "Exception error", e, None)


    # [OLED] - Draw a text
    def draw_text(self, points=None, text=None, size=None):
        check = self.points_check("text", points)
        if check["result"] == False:
            return check
        if text == None or type(text) != str:
            return self.return_msg(False, "Argument error", "Text is required", None)
        try:
            if size:
                self.oled.set_font(size=size)
            self.oled.draw_text(points, text)
            return self.return_msg(True, "Success", "Success", None)
        except Exception as e:
            return self.return_msg(False, "Exception error", e, None)


    # [OLED] - Draw an image
    def draw_image(self, filename=None):
        if filename == None:
            return self.return_msg(False, "Argument error", "Filename is required", None)
        else:
            ext = filename.rfind('.')
            file_ext = filename[ext+1:]
            if file_ext != 'png':
                return self.return_msg(False, "Extension error", "Only png files are available", None)
            file_exist = self.check_file(filename)
            if file_exist:
                img_check = self.oled.size_check(filename)
                if img_check[0] != 64 or img_check[1] != 128:
                    return self.return_msg(False, "Syntax error", "Only 128X64 sized files are available", None)
            else:
                return self.return_msg(False, "NotFound error", "The filename does not exist", None)
        try:
            self.oled.draw_image(filename)
            return self.return_msg(True, "Success", "Success", None)
        except Exception as e:
            return self.return_msg(False, "Exception error", e, None)


    # [OLED] - Draw a shpae
    def draw_figure(self, points=None, shape=None, fill=None):
        check = self.points_check("figure", points)
        if check["result"] == False:
            return check
        if shape == None or type(shape) != str:
            return self.return_msg(False, "Argument error", "Shape is required", None)
        try:
            if shape == 'rectangle':
                self.oled.draw_rectangle(points, fill)
            elif shape == 'circle':
                self.oled.draw_ellipse(points, fill)
            elif shape == 'line':
                self.oled.draw_line(points)
            else:
                return self.return_msg(False, "NotFound error", "The shape does not exist", None)
            return self.return_msg(True, "Success", "Success", None)
        except Exception as e:
            return self.return_msg(False, "Exception error", e, None)


    # [OLED] - Color inversion
    def invert(self):
        try:
            self.oled.invert()
            return self.return_msg(True, "Success", "Success", None)
        except Exception as e:
            return self.return_msg(False, "Exception error", e, None)


    # [OLED] - Show display
    def show_display(self):
        try:
            self.oled.show()
            return self.return_msg(True, "Success", "Success", None)
        except Exception as e:
            return self.return_msg(False, "Exception error", e, None)


    # [OLED] - Clear display
    def clear_display(self):
        try:
            self.oled.clear()
            return self.return_msg(True, "Success", "Success", None)
        except Exception as e:
            return self.return_msg(False, "Exception error", e, None)


    # [OLED] - Check points
    def points_check(self, mode, points=None):
        number = 2
        if mode == "figure":
            number = 4
        # points가 1개일 때 int -> tuple
        if points and type(points) == int:
            points = (points, )
        try: 
            if points == None or type(points) != tuple:
                return self.return_msg(False, "Argument error", "{} points are required".format(number), None)
            else:
                if len(points) != number:
                    return self.return_msg(False, "Syntax error", "{} points are required".format(number), None)
                for i in points:
                    if i < 0:
                        return self.return_msg(False, "Range error", "Points are only available positive number", None)
            return self.return_msg(True, "Success", "Success", None)
        except Exception as e:
            return self.return_msg(False, "Exception error", e, None)


    # [Speech] - Sentence translation
    def translate(self, string=None, to='ko'):
        to_list = ('ko', 'en')
        if string == None:
            return self.return_msg(False, "Argument error", "String is required", None)
        if to not in to_list:
            return self.return_msg(False, "Syntax error", "Translation is only available 'ko', 'en'", None)
        try:
            ret = self.speech.translate(string, to)
            return self.return_msg(True, "Success", "Success", ret)
        except Exception as e:
            return self.return_msg(False, "Exception error", e, None)


    # [Speech] - TTS
    def tts(self, string=None, filename='tts.mp3'):
        if string == None:
            return self.return_msg(False, "Argument error", "String is required", None)
        ext = filename.rfind('.')
        file_ext = filename[ext+1:]
        if file_ext != 'mp3':
            return self.return_msg(False, "Extension error", "TTS filename must be 'mp3'", None)
        voice_list= ('WOMAN_READ_CALM', 'MAN_READ_CALM', 'WOMAN_DIALOG_BRIGHT', 'MAN_DIALOG_BRIGHT')
        if '<speak>' not in string or '</speak>' not in string:
            return self.return_msg(False, "Syntax error", "Invalid string format", None)
        elif '<voice' in string and '</voice>' in string:
            voice_start = string.find('=')
            voice_end = string.find('>', voice_start)
            voice_name = string[voice_start+2:voice_end-1]
            if voice_name not in voice_list:
                return self.return_msg(False, "NotFound error", "The voice name does not exist", None)
        try:
            self.speech.tts(string, filename)
            return self.return_msg(True, "Success", "Success", None)
        except Exception as e:
            return self.return_msg(False, "Exception error", e, None)


    # [Speech] - STT
    def stt(self, filename='stream.wav', timeout=5):
        try:
            ret = self.speech.stt(filename, timeout)
            return self.return_msg(True, "Success", "Success", ret)
        except Exception as e:
            return self.return_msg(False, "Exception error", e, None)


    # [Speech] - Conversation
    def conversation(self, q=None):
        if q:
            if type(q) != str:
                return self.return_msg(False, "Syntax error", "Q is only available str type", None)
        else:
            return self.return_msg(False, "Argument error", "Q is required", None)
        try:
            ret = self.dialog.get_dialog(q)
            return self.return_msg(True, "Success", "Success", ret)
        except Exception as e:
            return self.return_msg(False, "Exception error", e, None)


    # [Vision] - start_camera thread
    def camera_on(self):
        vs = VideoStream().start()

        while True:
            if self.onair == False:
                vs.stop()
                break
            self.img = vs.read()
            img = self.img
            img = self.camera.convert_img(img, 128, 64)
            #_, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
            if self.flash:
                img = self.camera.rotate10(img)
                self.oled.draw_data(img)
                self.oled.show()
                time.sleep(0.3)
                self.flash = False
                continue
            self.oled.draw_data(img)
            self.oled.show()


    # [Vision] - Camera ON
    def start_camera(self):
        try:
            if self.onair:
                return self.return_msg(False, "Running error", "start_camera() is already running", None)
            self.onair = True
            t = Thread(target=self.camera_on, args=())
            t.daemon = True
            t.start()
            return self.return_msg(True, "Success", "Success", None)
        except Exception as e:
            return self.return_msg(False, "Exception error", e, None)


    # [Vision] - Camera OFF
    def stop_camera(self):
        try:
            self.onair = False
            time.sleep(0.5)
            return self.return_msg(True, "Success", "Success", None)
        except Exception as e:
            return self.return_msg(False, "Exception error", e, None)


    # [Vision] - Capture
    def capture(self, filename="capture.png"):
        file_list = ("png", "jpg", "jpeg", "bmp")
        ext = filename.rfind('.')
        file_ext = filename[ext+1:]
        if file_ext not in file_list:
            return self.return_msg(False, "Extension error", "Image filename must be 'png', 'jpg', 'jpeg', 'bmp'", None) 
        try:
            if self.onair:
                self.camera.imwrite(filename, self.img)
                self.flash = True
            else:
                img = self.camera.read()
                self.camera.imwrite(filename, img)
                img = self.camera.convert_img(img, 128, 64)
                #_, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
                self.oled.draw_data(img)
                self.oled.show()
            return self.return_msg(True, "Success", "Success", None)
        except Exception as e:
            return self.return_msg(False, "Exception error", e, None)


    # [Vision] - Detect object
    def search_object(self):
        try:
            img = self.check_onair()
            ret = self.detect.detect_object(img)
            return self.return_msg(True, "Success", "Success", ret)
        except Exception as e:
            return self.return_msg(False, "Exception error", e, None)


    # [Vision] - Detect QR/barcode
    def search_qr(self):
        try:
            img = self.check_onair()
            ret = self.detect.detect_qr(img)
            return self.return_msg(True, "Success", "Success", ret)
        except Exception as e:
            return self.return_msg(False, "Exception error", e, None)


    # [Vision] - Detect text
    def search_text(self):
        try:
            img = self.check_onair()
            ret = self.detect.detect_text(img)
            return self.return_msg(True, "Success", "Success", ret)
        except Exception as e:
            return self.return_msg(False, "Exception error", e, None)
        

    # [Vision] - Detect color
    def search_color(self):
        try:
            img = self.check_onair()
            height, width = img.shape[:2]
            img_hls = self.camera.bgr_hls(img)
            cnt = 0
            sum_hue = 0
            
            # 평균 패치 측정(j: Height, i: width)
            for i in range(50, width-50, 20):
                for j in range(50, height-50, 20):
                    sum_hue += (img_hls[j, i, 0]*2)
                    cnt += 1
            
            hue = round(sum_hue/cnt)

            if ( 0 <= hue <= 30) or (330 <=  hue <= 360):
                ans = "Red"
            elif (31 <=  hue <= 59):
                ans = "Orange"
            elif (60 <=  hue <= 85):
                ans = "Yellow"
            elif (86 <=  hue <= 159):
                ans = "Green"
            elif (160 <=  hue <= 209):
                ans = "Skyblue"
            elif (210 <=  hue <= 270):
                ans = "Blue"
            elif (271 <=  hue <= 290):
                ans = "Purple"
            elif (291<=  hue <= 329):
                ans = "Magenta"
            return self.return_msg(True, "Success", "Success", ans)
        except Exception as e:
            return self.return_msg(False, "Exception error", e, None)


    # [Vision] - Detect face
    def detect_face(self):
        try:
            img = self.check_onair()
            faceList = self.face.detect(img)
            if len(faceList) < 1:
                return self.return_msg(True, "Success", "Success", "No Face")
            return self.return_msg(True, "Success", "Success", faceList)
        except Exception as e:
            return self.return_msg(False, "Exception error", e, None)


    # [Vision] - Recognize face
    def search_face(self, filename="face.png"):
        max_w = -1
        selected_face = []
        if filename != None:
            file_list = ("png", "jpg", "jpeg", "bmp")
            ext = filename.rfind('.')
            file_ext = filename[ext+1:]
            if file_ext not in file_list:
                return self.return_msg(False, "Extension error", "Image filename must be 'png', 'jpg', 'jpeg', 'bmp'", None)
        try:
            img = self.check_onair()
            faceList = self.face.detect(img)
            
            if len(faceList) < 1:
                return self.return_msg(True, "Success", "Success", "No Face")
            for i, (x,y,w,h) in enumerate(faceList):
                if w > max_w:
                    max_w = w
                    idx = i

            ret = self.face.get_ageGender(img, faceList[idx])
            age = ret["age"]
            gender = ret["gender"]

            x,y,w,h = faceList[idx]
            self.camera.rectangle(img, (x, y), (x+w, y+h))

            ret = self.face.recognize(img, faceList[idx])
            name = "Guest" if ret == False else ret["name"]
            score = "-" if ret == False else ret["score"]
            result = self.camera.putText(img, "{} / {} {}".format(name, gender, age), (x-10, y-10), size=0.5)
            self.camera.imwrite(filename, result)
            return self.return_msg(True, "Success", "Success", {"name": name, "score": score, "gender": gender, "age": age})
        except Exception as e:
            return self.return_msg(False, "Exception error", e, None)


    # [Vision] - Train face
    def train_face(self, name=None):
        max_w = -1
        if name == None:
            return self.return_msg(False, "Argument error", "Name is required", None)
        try:
            img = self.check_onair()
            faces = self.face.detect(img)

            if len(faces) < 1:
                return self.return_msg(True, "Success", "Success", "No Face")

            for i, (x,y,w,h) in enumerate(faces):
                if w > max_w:
                    max_w = w
                    idx = i
            self.face.train_face(img, faces[idx], name)
            return self.return_msg(True, "Success", "Success", None)

        except Exception as e:
            return self.return_msg(False, "Exception error", e, None)


    # [Vision] - Get facedb
    def get_facedb(self):
        try:
            facedb = self.face.get_db()
            return self.return_msg(True, "Success", "Success", facedb)
        except Exception as e:
            return self.return_msg(False, "Exception error", e, None)


    # [Vision] - Reset facedb
    def init_facedb(self):
        try:
            self.face.init_db()
            return self.return_msg(True, "Success", "Success", None)
        except Exception as e:
            return self.return_msg(False, "Exception error", e, None)


    # [Vision] - Load facedb
    def load_facedb(self, filename=None):
        if filename == None:
            return self.return_msg(False, "Argument error", "Filename is required", None)
        else:
            file_exist = self.check_file(filename)
            if file_exist == False:
                return self.return_msg(False, "NotFound error", "The filename does not exist", None)
        try:
            self.face.load_db(filename)
            return self.return_msg(True, "Success", "Success", None)
        except Exception as e:
            return self.return_msg(False, "Exception error", e, None)


    # [Vision] - Save the facedb as a file
    def save_facedb(self, filename=None):
        if filename == None:
            return self.return_msg(False, "Argument error", "Filename is required", None)
        try:
            self.face.save_db(filename)
            return self.return_msg(True, "Success", "Success", None)
        except Exception as e:
            return self.return_msg(False, "Exception error", e, None)


    # [Vision] - Delete face in the facedb
    def delete_face(self, name=None):
        if name == None:
            return self.return_msg(False, "Argument error", "Name is required", None)
        try:
            ret = self.face.delete_face(name)
            if ret == False:
                return self.return_msg(ret, "NotFound error", "{} not exist in the facedb".format(name), None)
            return self.return_msg(ret, "Success", "Success", None)
        except Exception as e:
            return self.return_msg(False, "Exception error", e, None)


    # [Vision] - Determine image
    def check_onair(self):
        if self.onair:
            img = self.img
        else:
            img = self.camera.read()
        return img


    # Check file exist
    def check_file(self, filename):
        return Path(filename).is_file()

    
    # Return msg form
    def return_msg(self, status, errcode, errmsg, data):
        global code_list
        return {"result": status, "errcode": code_list[errcode], "errmsg": errmsg, "data": data}


    # Getting the meaning of error code
    def get_codeMean(self, errcode):
        global code_list
        n_list = {value:key for key, value in code_list.items()}

        if errcode in n_list.keys():
            return self.return_msg(True, "Success", "Success", n_list[errcode])
        return self.return_msg(False, "NotFound error", "Error code {} does not exist".format(errcode), None)
