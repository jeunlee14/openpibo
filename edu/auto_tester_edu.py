import sys, os, time, pytest

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from utils.config import Config as cfg
from pathlib import Path

sys.path.append(cfg.OPENPIBO_PATH + '/edu')
from pibo import Edu_Pibo

pibo = Edu_Pibo()

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

motor_range = [25,35,80,30,50,25,25,35,80,30]


def res_form(result=True, errtype='Success', errmsg='Success', data=None):
    errcode = code_list[errtype]
    res = {'result': result, 'errcode': errcode, 'errmsg': errmsg, 'data': data}
    return res

# [Audio] Test
class TestPlayAudio:
    def test_invalid_extension_filename(self):
        res = pibo.play_audio(filename=cfg.TESTDATA_PATH+"/test.mp4", out='local', volume='-2000', background=True)
        assert res == res_form(False, "Extension error", "Audio filename must be 'mp3', 'wav'", None)

    def test_invalid_not_found_filename(self):
        res = pibo.play_audio(filename="notfound.mp3", out='local', volume='-2000', background=True)
        assert res == res_form(False, "NotFound error", "The filename does not exist", None)

    def test_invalid_argument_filename(self):
        res = pibo.play_audio(filename=None, out='local', volume='-2000', background=True)
        assert res == res_form(False, "Argument error", "Filename is required", None)

    def test_invalid_not_found_output(self):
        res = pibo.play_audio(filename=cfg.TESTDATA_PATH+"/test.mp3", out='notfound', volume='-2000', background=True)
        assert res == res_form(False, "NotFound error", "Output device must be 'local', 'hdmi', 'both'", None)

    def test_valid(self):
        res = pibo.play_audio(filename=cfg.TESTDATA_PATH+"/test.mp3", out='local', volume='-2000', background=True)
        assert res == res_form()


class TestStopAudio:
    def test_valid(self):
        res = pibo.stop_audio()
        assert res == res_form()

# [Neopixel] Test
"""
# alpha_cnt 지역변수로 변경 합니다.
"""
class TestIsAlpha:
    def test_valid_color_both(self):
        res = pibo.isAlpha('red')
        assert res == True

    def test_valid_color_each(self):
        res = pibo.isAlpha('green', 'blue')
        assert res == True

    """
    # isAlpha 현재 여러 요청값 중 하나만 alphabet이어도 True 출력. 에러 출력이 필요합니다.
    def test_invalid_color_num(self):
        res = pibo.isAlpha(255, 'blue')
        assert res == False
    """

    def test_invalid_no_alpha(self):
        res = pibo.isAlpha(255)
        assert res == False


class TestEyeOn:
    def test_invalid_argument_color(self):
        res = pibo.eye_on()
        assert res == res_form(False, "Argument error", "RGB or Color is required", None)

    def test_invalid_range_less_rgb(self):
        res = pibo.eye_on(-1, 0, 0)
        assert res == res_form(False, "Range error", "RGB value should be 0~255", None)

    def test_invalid_range_over_rgb(self):
        res = pibo.eye_on(256, 255, 255)
        assert res == res_form(False, "Range error", "RGB value should be 0~255", None)

    def test_invalid_syntax_rgb_less(self):
        res = pibo.eye_on(255, 255)
        assert res == res_form(False, "Syntax error", "Only 3 or 6 values can be entered", None)

    def test_invalid_syntax_rgb_over(self):
        res = pibo.eye_on(255, 255, 255, 255)
        assert res == res_form(False, "Syntax error", "Only 3 or 6 values can be entered", None)

    def test_invalid_not_found_color(self):
        color = 'notfound'
        res = pibo.eye_on(color)
        assert res == res_form(False, "NotFound error", "{} does not exist in the colordb".format(color), None)

    def test_invalid_not_found(self):
        color = ('notfound', 'red')
        res = pibo.eye_on(color[0], color[1])
        assert res == res_form(False, "NotFound error", "{} does not exist in the colordb".format(color[0]), None)

    def test_invalid_not_found(self):
        color = ('red', 'notfound')
        res = pibo.eye_on(color[0], color[1])
        assert res == res_form(False, "NotFound error", "{} does not exist in the colordb".format(color[1]), None)

    def test_invalid_syntax_colorname_over(self):
        color = ('red', 'greed', 'blue')
        res = pibo.eye_on(color[0], color[1], color[2])
        assert res == res_form(False, "Syntax error", "Only 2 colors can be entered", None)

    def test_valid_rgb3(self):
        res = pibo.eye_on(255, 0, 0)
        assert res == res_form()

    def test_valid_rgb6(self):
        res = pibo.eye_on(0, 255, 0, 0, 0, 255)
        assert res == res_form()

    def test_valid_colorname1(self):
        res = pibo.eye_on('red')
        assert res == res_form()

    def test_valid_colorname2(self):
        res = pibo.eye_on('green', 'blue')
        assert res == res_form()


class TestEyeOff:
    def test_valid(self):
        res = pibo.eye_off()
        assert res == res_form()


class TestAddColor:
    def test_invalid_argument_color(self):
        res = pibo.add_color(None, 85, 170, 255)
        assert res == res_form(False, "Argument error", "Color is required", None)

    def test_invalid_argument(self):
        res = pibo.add_color(color='sky')
        assert res == res_form(False, "Argument error", "RGB value is required", None)

    def test_invalid_syntax_rgb_less(self):
        res = pibo.add_color('sky', 85, 170)
        assert res == res_form(False, "Syntax error", "3 values are required(R,G,B)", None)

    def test_invalid_syntax_rgb_over(self):
        res = pibo.add_color('sky', 0, 85, 170, 255)
        assert res == res_form(False, "Syntax error", "3 values are required(R,G,B)", None)

    def test_invalid_range_less_rgb(self):
        res = pibo.add_color('sky', -1, 170, 255)
        assert res == res_form(False, "Range error", "RGB value should be 0~255", None)

    def test_invalid_range_over_rgb(self):
        res = pibo.add_color('sky', 85, 170, 256)
        assert res == res_form(False, "Range error", "RGB value should be 0~255", None)

    def test_invalid_exist_color(self):
        color = 'red'
        res = pibo.add_color(color, 255, 0, 0)
        assert res == res_form(False, "Exist error", "{} is already exist".format(color), None)

    def test_valid(self):
        res = pibo.add_color('sky', 85, 170, 255)
        assert res == res_form()


class TestGetColordb:
    def test_valid(self):
        res = pibo.get_colordb()
        assert res == res_form(True, "Success", "Success", pibo.colordb)


class TestInitColordb:
    def test_valid(self):
        res = pibo.init_colordb()
        assert res == res_form()


class TestSaveColordb:
    def test_invalid_argument_filename(self):
        res = pibo.save_colordb(filename=None)
        assert res == res_form(False, "Argument error", "Filename is required", None)

    def test_valid(self):
        res = pibo.save_colordb(filename='test')
        assert res == res_form()


class TestLoadColordb:
    def test_invalid_argument_filename(self):
        res = pibo.load_colordb(filename=None)
        assert res == res_form(False, "Argument error", "Filename is required", None)

    def test_invalid_not_found_filename(self):
        res = pibo.load_colordb(filename='notfound')
        assert res == res_form(False, "NotFound error", "The filename does not exist", None)

    def test_valid(self):
        res = pibo.load_colordb(filename='test')
        assert res == res_form()


class TestDeleteColor:
    def test_invalid_argument_color(self):
        res = pibo.delete_color(color=None)
        assert res == res_form(False, "Argument error", "Color is required", None)

    def test_valid(self):
        res = pibo.delete_color(color='red')
        assert res == res_form()

    def test_invalid_not_found_color(self):
        color = 'notfound'
        res = pibo.delete_color(color=color)
        assert res == res_form(False, "NotFound error", "{} not exist in the colordb".format(color), None)

# [Device] Test
class TestCheckDevice:
    def test_invalid_not_found_system(self):
        res = pibo.check_device(system='notfound')
        assert res == res_form(False, "NotFound error", "System must be 'battery', 'system'", None)

    def test_invalid_argument_system(self):
        res = pibo.check_device(system=None)
        assert res == res_form(False, "Argument error", "Enter the device name to check", None)

    def test_valid_battery(self):
        res = pibo.check_device(system='battery')
        assert res == res_form(True, "Success", "Success", res['data'])

    def test_valid_system(self):
        res = pibo.check_device(system='system')
        assert res == res_form(True, "Success", "Success", res['data'])


class TestStartDevices:
    def test_invalid_argument_func(self):
        res = pibo.start_devices(func=None)
        assert res == res_form(False, "Argument error", "Func is required", None)

    def test_valid(self):
        res = pibo.start_devices(func=lambda x: print(x))
        assert res == res_form()

    # 위 test_valid에서 thread를 쓰고있기 때문에 running error가 발생.
    def test_invalid_running(self):
        res = pibo.start_devices(func=lambda x: print(x))
        assert res == res_form(False, "Running error", "start_devices() is already running", None)


class TestStopDevices:
    def test_valid(self):
        res = pibo.stop_devices()
        assert res == res_form()

# [Motion] Test
class TestMotor:
    def test_invalid_range_less_n(self):
        res = pibo.motor(n=-1, position=0, speed=0, accel=0)
        assert res == res_form(False, "Range error", "Channel value should be 0~9", None)

    def test_invalid_range_over_n(self):
        res = pibo.motor(n=10, position=0, speed=0, accel=0)
        assert res == res_form(False, "Range error", "Channel value should be 0~9", None)

    def test_invalid_argument_n(self):
        res = pibo.motor(n=None, position=0, speed=0, accel=0)
        assert res == res_form(False, "Argument error", "Channel is required", None)

    def test_invalid_range_less_position(self):
        n = 0
        res = pibo.motor(n=n, position=-26, speed=0, accel=0)
        assert res == res_form(False, "Range error", "The position range of channel {} is -{} ~ {}".format(n, motor_range[n], motor_range[n]), None)

    def test_invalid_range_over_position(self):
        n = 0
        res = pibo.motor(n=n, position=26, speed=0, accel=0)
        assert res == res_form(False, "Range error", "The position range of channel {} is -{} ~ {}".format(n, motor_range[n], motor_range[n]), None)

    def test_invalid_argument_position(self):
        res = pibo.motor(n=0, position=None, speed=0, accel=0)
        assert res == res_form(False, "Argument error", "Position is required", None)

    def test_invalid_range_less_speed(self):
        res = pibo.motor(n=0, position=0, speed=-1, accel=0)
        assert res == res_form(False, "Range error", "Speed value should be 0~255", None)

    def test_invalid_range_over_speed(self):
        res = pibo.motor(n=0, position=0, speed=256, accel=0)
        assert res == res_form(False, "Range error", "Speed value should be 0~255", None)

    def test_invalid_range_less_accel(self):
        res = pibo.motor(n=0, position=0, speed=0, accel=-1)
        assert res == res_form(False, "Range error", "Acceleration value should be 0~255", None)

    def test_invalid_range_over_accel(self):
        res = pibo.motor(n=0, position=0, speed=0, accel=256)
        assert res == res_form(False, "Range error", "Acceleration value should be 0~255", None)

    def test_valid(self):
        res = pibo.motor(n=0, position=0, speed=10, accel=10)
        assert res == res_form()


class TestMotors:
    def test_valid(self):
        positions = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        speed = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
        accel = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
        res = pibo.motors(positions=positions, speed=speed, accel=accel)
        assert res == res_form()

    def test_invalid_syntax_less_positions(self):
        positions = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        speed = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        accel = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        res = pibo.motors(positions=positions, speed=speed, accel=accel)
        assert res == res_form(False, "Syntax error", "10 positions are required", None)

    def test_invalid_syntax_less_speed(self):
        positions = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        speed = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        accel = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        res = pibo.motors(positions=positions, speed=speed, accel=accel)
        assert res == res_form(False, "Syntax error", "10 speeds are required", None)

    def test_invalid_syntax_less_accel(self):
        positions = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        speed = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        accel = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        res = pibo.motors(positions=positions, speed=speed, accel=accel)
        assert res == res_form(False, "Syntax error", "10 accelerations are required", None)

    def test_invalid_syntax_over_positions(self):
        positions = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        speed = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        accel = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        res = pibo.motors(positions=positions, speed=speed, accel=accel)
        assert res == res_form(False, "Syntax error", "10 positions are required", None)

    def test_invalid_syntax_over_speed(self):
        positions = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        speed = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        accel = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        res = pibo.motors(positions=positions, speed=speed, accel=accel)
        assert res == res_form(False, "Syntax error", "10 speeds are required", None)

    def test_invalid_syntax_over_accel(self):
        positions = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        speed = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        accel = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        res = pibo.motors(positions=positions, speed=speed, accel=accel)
        assert res == res_form(False, "Syntax error", "10 accelerations are required", None)

    def test_invalid_range_less_positions(self):
        positions = [-26, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        speed = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        accel = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        i = 0
        res = pibo.motors(positions=positions, speed=speed, accel=accel)
        assert res == res_form(False, "Range error", "The position range of channel {} is -{} ~ {}".format(i, motor_range[i], motor_range[i]), None)

    def test_invalid_range_over_positions(self):
        positions = [26, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        speed = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        accel = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        i = 0
        res = pibo.motors(positions=positions, speed=speed, accel=accel)
        assert res == res_form(False, "Range error", "The position range of channel {} is -{} ~ {}".format(i, motor_range[i], motor_range[i]), None)

    def test_invalid_range_less_speed(self):
        positions = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        speed = [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        accel = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        mode = 'speed'
        res = pibo.motors(positions=positions, speed=speed, accel=accel)
        assert res == res_form(False, "Range error", "{} value should be 0~255".format(mode.capitalize()), None)

    def test_invalid_range_less_accel(self):
        positions = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        speed = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        accel = [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        mode = 'acceleration'
        res = pibo.motors(positions=positions, speed=speed, accel=accel)
        assert res == res_form(False, "Range error", "{} value should be 0~255".format(mode.capitalize()), None)

    def test_invalid_range_over_speed(self):
        positions = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        speed = [256, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        accel = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        mode = 'speed'
        res = pibo.motors(positions=positions, speed=speed, accel=accel)
        assert res == res_form(False, "Range error", "{} value should be 0~255".format(mode.capitalize()), None)

    def test_invalid_range_over_accel(self):
        positions = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        speed = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        accel = [256, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        mode = 'acceleration'
        res = pibo.motors(positions=positions, speed=speed, accel=accel)
        assert res == res_form(False, "Range error", "{} value should be 0~255".format(mode.capitalize()), None)


class TestMotorsMovetime:
    def test_invalid_syntax_less_positions(self):
        positions = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        res = pibo.motors_movetime(positions=positions, movetime=0)
        assert res == res_form(False, "Syntax error", "10 positions are required", None)

    def test_invalid_syntax_over_positions(self):
        positions = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        res = pibo.motors_movetime(positions=positions, movetime=0)
        assert res == res_form(False, "Syntax error", "10 positions are required", None)

    def test_invalid_range_less_positions(self):
        positions = [-26, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        i = 0
        res = pibo.motors_movetime(positions=positions, movetime=0)
        assert res == res_form(False, "Range error", "The position range of channel {} is -{} ~ {}".format(i, motor_range[i], motor_range[i]), None)

    def test_invalid_range_over_positions(self):
        positions = [26, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        i = 0
        res = pibo.motors_movetime(positions=positions, movetime=0)
        assert res == res_form(False, "Range error", "The position range of channel {} is -{} ~ {}".format(i, motor_range[i], motor_range[i]), None)

    def test_invalid_range_less_movetime(self):
        positions = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        res = pibo.motors_movetime(positions=positions, movetime=-1)
        assert res == res_form(False, "Range error", "Movetime is only available positive number", None)

    def test_valid(self):
        positions = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        res = pibo.motors_movetime(positions=positions, movetime=0)
        assert res == res_form()


class TestGetMotion:
    def test_valid(self):
        res = pibo.get_motion(name="stop")
        assert res == res_form(True, "Success", "Success", res['data'])


class TestSetMotion:
    def test_invalid_argument_name(self):
        res = pibo.set_motion(name=None, cycle=1)
        assert res == res_form(False, "Argument error", "Name is required", None)

    def test_invalid_not_found_name(self):
        name='notfound'
        res = pibo.set_motion(name=name, cycle=1)
        assert res == res_form(False, "NotFound error", "{} not exist in the motor profile".format(name), None)

    def test_valid(self):
        res = pibo.set_motion(name='stop', cycle=1)
        assert res == res_form(True, "Success", "Success", None)


class TestCheckMotor:
    def test_invalid_syntax(self):
        mode = "speed"
        values = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        res = pibo.check_motor(mode, values)
        assert res == res_form(False, "Syntax error", "10 {}s are required".format(mode), None)

    def test_invalid_range(self):
        mode = "position"
        values = [26, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        i = 0
        res = pibo.check_motor(mode, values)
        assert res == res_form(False, "Range error", "The position range of channel {} is -{} ~ {}".format(i, motor_range[i], motor_range[i]), None)

    def test_invalid_range_less_speed(self):
        mode = "speed"
        values = [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        res = pibo.check_motor(mode, values)
        assert res == res_form(False, "Range error", "{} value should be 0~255".format(mode.capitalize()), None)

    def test_invalid_range_over_speed(self):
        mode = "speed"
        values = [256, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        res = pibo.check_motor(mode, values)
        assert res == res_form(False, "Range error", "{} value should be 0~255".format(mode.capitalize()), None)

    def test_invalid_range_less_accel(self):
        mode = "acceleration"
        values = [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        res = pibo.check_motor(mode, values)
        assert res == res_form(False, "Range error", "{} value should be 0~255".format(mode.capitalize()), None)

    def test_invalid_range_over_accel(self):
        mode = "acceleration"
        values = [256, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        res = pibo.check_motor(mode, values)
        assert res == res_form(False, "Range error", "{} value should be 0~255".format(mode.capitalize()), None)

    def test_valid(self):
        mode = "position"
        values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        res = pibo.check_motor(mode, values)
        assert res == res_form()

    def test_valid(self):
        mode = "speed"
        values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        res = pibo.check_motor(mode, values)
        assert res == res_form()

    def test_valid(self):
        mode = "acceleration"
        values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        res = pibo.check_motor(mode, values)
        assert res == res_form()

# [OLED] Test
class TestDrawText:
    def test_invalid_argument_text_points(self):
        res = pibo.draw_text(points=None, text='hello', size=None)
        assert res == res_form(False, "Argument error", "2 points are required", None)

    def test_invalid_syntax_less_text_points(self):
        res = pibo.draw_text(points=(0,), text='hello', size=None)
        assert res == res_form(False, "Syntax error", "2 points are required", None)

    def test_invalid_syntax_over_text_points(self):
        res = pibo.draw_text(points=(0, 0, 0), text='hello', size=None)
        assert res == res_form(False, "Syntax error", "2 points are required", None)

    def test_invalid_range_points(self):
        res = pibo.draw_text(points=(-1, 0), text='hello', size=None)
        assert res == res_form(False, "Range error", "Points are only available positive number", None)

    def test_invalid_argument_text(self):
        res = pibo.draw_text(points=(0, 0), text=None, size=None)
        assert res == res_form(False, "Argument error", "Text is required", None)

    def test_valid(self):
        res = pibo.draw_text(points=(0, 0), text='hello', size=None)
        assert res == res_form()


class TestDrawImage:
    def test_invalid_argument_filename(self):
        res = pibo.draw_image(filename=None)
        assert res == res_form(False, "Argument error", "Filename is required", None)

    def test_invalid_extension_filename(self):
        res = pibo.draw_image(filename=cfg.TESTDATA_PATH +"/bus.jpg")
        assert res == res_form(False, "Extension error", "Only png files are available", None)

    def test_invalid_syntax_filesize(self):
        res = pibo.draw_image(filename=cfg.TESTDATA_PATH +"/64x64.png")
        assert res == res_form(False, "Syntax error", "Only 128X64 sized files are available", None)

    def test_invalid_not_found_filename(self):
        res = pibo.draw_image(filename=cfg.TESTDATA_PATH +"/notfound.png")
        assert res == res_form(False, "NotFound error", "The filename does not exist", None)

    def test_valid(self):
        res = pibo.draw_image(filename=cfg.TESTDATA_PATH +"/clear.png")
        assert res == res_form()


class TestDrawFigure:
    def test_invalid_argument_figure_points(self):
        res = pibo.draw_figure(points=None, shape='line', fill=True)
        assert res == res_form(False, "Argument error", "4 points are required", None)

    def test_invalid_syntax_less_figure_points(self):
        res = pibo.draw_figure(points=(0, 0, 0), shape='line', fill=True)
        assert res == res_form(False, "Syntax error", "4 points are required", None)

    def test_invalid_syntax_over_figure_points(self):
        res = pibo.draw_figure(points=(0, 0, 0, 0, 0), shape='line', fill=True)
        assert res == res_form(False, "Syntax error", "4 points are required", None)

    def test_invalid_range_points(self):
        res = pibo.draw_figure(points=(-1, 0, 0, 0), shape='line', fill=True)
        assert res == res_form(False, "Range error", "Points are only available positive number", None)

    def test_invalid_argument_shape(self):
        res = pibo.draw_figure(points=(0, 0, 0, 0), shape=None, fill=True)
        assert res == res_form(False, "Argument error", "Shape is required", None)

    def test_invalid_not_found_shape(self):
        res = pibo.draw_figure(points=(0, 0, 0, 0), shape='notfound', fill=True)
        assert res == res_form(False, "NotFound error", "The shape does not exist", None)

    def test_valid_rectangle(self):
        res = pibo.draw_figure(points=(0, 0, 0, 0), shape='rectangle', fill=True)
        assert res == res_form()

    def test_valid_circle(self):
        res = pibo.draw_figure(points=(0, 0, 0, 0), shape='circle', fill=True)
        assert res == res_form()

    def test_valid_line(self):
        res = pibo.draw_figure(points=(0, 0, 0, 0), shape='line', fill=True)
        assert res == res_form()


class TestInvert:
    def test_valid(self):
        res = pibo.invert()
        assert res == res_form()


class TestShowDisplay:
    def test_valid(self):
        res = pibo.show_display()
        assert res == res_form()


class TestClearDisplay:
    def test_valid(self):
        res = pibo.clear_display()
        assert res == res_form()

"""
# points 범위를 (128X64) 로 제한하는 것이 좋지 않을까요??
"""
class TestPointsCheck:
    def test_invalid_argument_text_points(self):
        mode = 'text'
        res = pibo.points_check(mode, points=None)
        assert res == res_form(False, "Argument error", "2 points are required", None)

    def test_invalid_argument_figure_points(self):
        mode = 'figure'
        res = pibo.points_check(mode, points=None)
        assert res == res_form(False, "Argument error", "4 points are required", None)

    """
    # 현재 points=0으로 넣었을 때 points=(0,)로 바뀌지 않는 문제 발생.
    # ~~pibo.py (537line) [if points] => [if points != None]으로 변경했습니다.~~
    ## 아예 int를 tuple로 변경하는 코드를 삭제하는 방향으로 접근하기로 함!
    def test_invalid_syntax_less_text_points_zero(self):
        mode = 'text'
        res = pibo.points_check(mode, points=0)
        assert res == res_form(False, "Syntax error", "2 points are required", None)
    """

    def test_invalid_syntax_less_text_points(self):
        mode = 'text'
        res = pibo.points_check(mode, points=(0,))
        assert res == res_form(False, "Syntax error", "2 points are required", None)

    def test_invalid_syntax_over_text_points(self):
        mode = 'text'
        res = pibo.points_check(mode, points=(0, 0, 0))
        assert res == res_form(False, "Syntax error", "2 points are required", None)

    def test_invalid_syntax_less_figure_points(self):
        mode = 'figure'
        res = pibo.points_check(mode, points=(0,))
        assert res == res_form(False, "Syntax error", "4 points are required", None)

    def test_invalid_syntax_over_figure_points(self):
        mode = 'figure'
        res = pibo.points_check(mode, points=(0, 0, 0, 0, 0))
        assert res == res_form(False, "Syntax error", "4 points are required", None)

    def test_invalid_range_text_points(self):
        mode = 'text'
        res = pibo.points_check(mode, points=(-1, 0))
        assert res == res_form(False, "Range error", "Points are only available positive number", None)

    def test_invalid_range_figure_points(self):
        mode = 'figure'
        res = pibo.points_check(mode, points=(-1, 0, 0, 0))
        assert res == res_form(False, "Range error", "Points are only available positive number", None)

    def test_valid_text_points(self):
        mode = 'text'
        res = pibo.points_check(mode, points=(0, 0))
        assert res == res_form()

    def test_valid_figure_points(self):
        mode = 'figure'
        res = pibo.points_check(mode, points=(0, 0, 0, 0))
        assert res == res_form()

# [Speech] Test
class TestTranslate:
    def test_invalid_argument_string(self):
        res = pibo.translate(string=None, to='ko')
        assert res == res_form(False, "Argument error", "String is required", None)

    def test_invalid_syntax_to(self):
        res = pibo.translate(string='안녕하세요', to='xx')
        assert res == res_form(False, "Syntax error", "Translation is only available 'ko', 'en'", None)

    def test_valid(self):
        res = pibo.translate(string='안녕하세요', to='ko')
        # '안녕하세요' -> '안녕하세요 '로 번역됨. (띄어쓰기 하나 추가됨.)
        # 변역 모델 업데이트시 테스트케이스 변경이 필요할 수 있음.
        assert res == res_form(True, "Success", "Success", '안녕하세요 ')


class TestTts:
    def test_invalid_argument_string(self):
        res = pibo.tts(string=None, filename='tts.mp3')
        assert res == res_form(False, "Argument error", "String is required", None)

    def test_invalid_extension_string(self):
        res = pibo.tts(string="<speak><voice name='WOMAN_READ_CALM'>안녕. 나는 파이보야.<break time='500ms'/></voice></speak>", filename='tts.mp4')
        assert res == res_form(False, "Extension error", "TTS filename must be 'mp3'", None)

    def test_invalid_syntax_string(self):
        res = pibo.tts(string="<voice name='WOMAN_READ_CALM'>안녕. 나는 파이보야.<break time='500ms'/></voice>", filename='tts.mp3')
        assert res == res_form(False, "Syntax error", "Invalid string format", None)

    def test_invalid_not_found(self):
        res = pibo.tts(string="<speak><voice name='NOTFOUND'>안녕. 나는 파이보야.<break time='500ms'/></voice></speak>", filename='tts.mp3')
        assert res == res_form(False, "NotFound error", "The voice name does not exist", None)

    def test_valid(self):
        res = pibo.tts(string="<speak><voice name='WOMAN_READ_CALM'>안녕. 나는 파이보야.<break time='500ms'/></voice></speak>", filename='tts.mp3')
        assert res == res_form()


class TestStt:
    def test_valid(self):
        res = pibo.stt(timeout=1)
        assert res == res_form(True, "Success", "Success", res['data'])


class TestConversation:
    def test_invalid_syntax(self):
        res = pibo.conversation(q=123)
        assert res == res_form(False, "Syntax error", "Q is only available str type", None)

    def test_invalid_argument(self):
        res = pibo.conversation(q=None)
        assert res == res_form(False, "Argument error", "Q is required", None)

    def test_valid(self):
        res = pibo.conversation(q='안녕')
        assert res == res_form(True, "Success", "Success", res['data'])

# extra test
class TestCheckFile:
    def test_valid(self):
        filename = 'test'
        res = pibo.check_file(filename)
        assert res == True
    
    def test_invalid(self):
        filename = 'notfound.png'
        res = pibo.check_file(filename)
        assert res == False


class TestReturnMsg:
    def test_valid(self):
        status = True
        errcode = 'Success'
        errmsg = 'errmsg'
        data = 'data'
        res = pibo.return_msg(status, errcode, errmsg, data)
        assert res == {"result": status, "errcode": code_list[errcode], "errmsg": errmsg, "data": data}


def test_end():
    pibo.eye_on('white')
    os.system('sudo pkill omxplayer')
    os.remove('test')
    os.remove('tts.mp3')
    os.remove('stream.wav')
    assert True