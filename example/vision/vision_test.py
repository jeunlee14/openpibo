import sys
sys.path.append('/home/pi/openpibo/lib')

from vision.visionlib import cCamera
from vision.visionlib import cFace

def test_f():
    cam = cCamera()
    disp = cFace()


if __name__ == "__main__":
    test_f()
