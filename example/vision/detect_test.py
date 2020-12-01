import sys
sys.path.append('/home/pi/openpibo/lib')

from vision.visionlib import cCamera
from vision.visionlib import cDetect

def test_func():
  # instance
  cam = cCamera()
  det = cDetect()

  # Capture / Read file
  img = cam.read()
  #img = cam.imread("image.jpg")

  print("Object Detect: ", det.detect_object(img))
  print("Qr Detect:", det.detect_qr(img))
  print("Text Detect:", det.detect_text(img))

if __name__ == "__main__":
  test_func()
