import sys
sys.path.append('/home/pi/openpibo/lib')

from vision.visionlib import cCamera

def test_func():
  # instance
  cam = cCamera()

  # For streaming
  cam.streaming(timeout=3)

  # Capture / Read file
  img = cam.read()
  #img = cam.imread("/home/pi/test.jpg")

  # Draw rectangle, Text
  cam.rectangle(img, (100,100), (300,300))
  cam.putText(img, "Hello Camera", (50, 50))

  # Write
  cam.imwrite("test.jpg", img)

  # display (only GUI)
  cam.imshow(img, "TITLE")
  cam.imshow(cam.cartoonize(img), "CARTOON")
  cam.waitKey(3000)

if __name__ == "__main__":
  test_func()
