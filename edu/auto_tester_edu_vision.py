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


def res_form(result=True, errtype='Success', errmsg='Success', data=None):
    errcode = code_list[errtype]
    res = {'result': result, 'errcode': errcode, 'errmsg': errmsg, 'data': data}
    return res

# [Vision] Test
class TestStartCamera:
    def test_valid(self):
        res = pibo.start_camera()
        time.sleep(3)
        assert res == res_form()

    # 위 test_valid함수의 실행으로 start_camera()가 실행중이기 때문에 에러 발생
    def test_invalid_running(self):
        res = pibo.start_camera()
        assert res == res_form(False, "Running error", "start_camera() is already running", None)

        
class TestCapture:
    def test_invalid_extension_filename(self):
        res = pibo.capture(filename="capture.ext")
        assert res == res_form(False, "Extension error", "Image filename must be 'png', 'jpg', 'jpeg', 'bmp'", None)

    def test_valid(self):
        res = pibo.capture()
        assert res == res_form()


class TestSearchObject:
    def test_valid(self):
        res = pibo.search_object()
        assert res == res_form(True, "Success", "Success", res['data'])


class TestSearchQr:
    def test_valid(self):
        res = pibo.search_qr()
        assert res == res_form(True, "Success", "Success", res['data'])


class TestSearchText:
    def test_valid(self):
        res = pibo.search_text()
        assert res == res_form(True, "Success", "Success", res['data'])


class TestSearchColor:
    def test_valid(self):
        res = pibo.search_color()
        assert res == res_form(True, "Success", "Success", res['data'])


class TestDetectFace:
    def test_valid(self):
        res = pibo.detect_face()
        assert res == res_form(True, "Success", "Success", res['data'])


class TestSearchFace:
    def test_invalid_extension_filename(self):
        res = pibo.search_face(filename="face.img")
        assert res == res_form(False, "Extension error", "Image filename must be 'png', 'jpg', 'jpeg', 'bmp'", None)

    def test_valid(self):
        res = pibo.search_face(filename="face.png")
        assert res == res_form(True, "Success", "Success", res['data'])


class TestTrainFace:
    def test_invalid_argument_name(self):
        res = pibo.train_face(name=None)
        assert res == res_form(False, "Argument error", "Name is required", None)

    def test_valid(self):
        name = 'tester'
        res = pibo.train_face(name=name)
        if res == res_form(True, "Success", "Success", "No Face"):
            img = pibo.camera.imread(cfg.TESTDATA_PATH+'/vision_sample3.jpg')
            pibo.face.train_face(img, [0, 0, 457, 512], name)
            assert True
        elif res == res_form(True, "Success", "Success", res['data']):
            assert True
        else:
            assert False


class TestGetFacedb:
    def test_valid(self):
        res = pibo.get_facedb()
        assert res == res_form(True, "Success", "Success", res['data'])


class TestDeleteFace:
    def test_invalid_argument_name(self):
        res = pibo.delete_face(name=None)
        assert res == res_form(False, "Argument error", "Name is required", None)

    def test_invalid_not_found_name(self):
        name = 'notfounddb'
        res = pibo.delete_face(name=name)
        assert res == res_form(False, "NotFound error", "{} not exist in the facedb".format(name), None)

    def test_valid(self):
        res = pibo.delete_face(name='tester')
        assert res == res_form(True, "Success", "Success", None)


class TestSaveFacedb:
    def test_invalid_argument_filename(self):
        res = pibo.save_facedb(filename=None)
        assert res == res_form(False, "Argument error", "Filename is required", None)

    def test_valid(self):
        res = pibo.save_facedb(filename='./facedb')
        assert res == res_form()


class TestLoadFacedb:
    def test_invalid_argument_filename(self):
        res = pibo.load_facedb(filename=None)
        assert res == res_form(False, "Argument error", "Filename is required", None)

    def test_invalid_not_found_filename(self):
        res = pibo.load_facedb(filename='notfound')
        assert res == res_form(False, "NotFound error", "The filename does not exist", None)

    def test_valid(self):
        res = pibo.load_facedb(filename='./facedb')
        assert res == res_form()


class TestInitFacedb:
    def test_valid(self):
        res = pibo.init_facedb()
        assert res == res_form()


class TestCheckOnair:
    def test_valid(self):
        res = pibo.check_onair()
        assert res[0][0][0]


class TestStopCamera:
    def test_valid(self):
        res = pibo.stop_camera()
        assert res == res_form()


def test_end():
    pibo.clear_display()
    os.remove('capture.png')
    os.remove('facedb')
    try:
        os.remove('face.png')
    except:
        pass
    assert True