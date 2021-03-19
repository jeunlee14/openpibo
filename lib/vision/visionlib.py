import cv2
import dlib
import numpy as np
import pytesseract
from pyzbar import pyzbar
import pickle,os,time
from vision.stream import VideoStream

#class cVision:
  #model_path = "/home/pi/openpibo/lib/vision/models/"
  #data_path = "/home/pi/openpibo/data/"

class cCamera:
  def __init__(self):
    os.system('v4l2-ctl -c vertical_flip=1,horizontal_flip=1,white_balance_auto_preset=3')

  def imread(self, filename):
    return cv2.imread(filename)

  def read(self, w=640, h=480):
    vs = VideoStream(width=w, height=h).start()
    img = vs.read()
    vs.stop()
    return img

  def imwrite(self, filename, img):
    return cv2.imwrite(filename, img)

  def imshow(self, img, title="IMAEGE"):
    # only GUI mode
    return cv2.imshow(title, img)

  def waitKey(self, timeout=1000):
    #timeout: millisecond
    return cv2.waitKey(timeout)

  def streaming(self, w=640, h=480, timeout=5):
    vs = VideoStream(width=w, height=h).start()
    t = time.time()

    while True:
      img = vs.read()
      cv2.imshow("show", img)
      cv2.waitKey(1)
      if time.time() - t > timeout:
        break
    vs.stop()
    return True

  def rectangle(self, img, p1, p2, color=(255,255,255), tickness=1):
    #p1: (startX, startY) / p2: (endX, endY)
    return cv2.rectangle(img, p1, p2, color, tickness)

  def putText(self, img, text, p, size=1, color=(255,255,255), tickness=1):
    #p: (startX, startY)
    return cv2.putText(img, text, p, cv2.FONT_HERSHEY_SIMPLEX, size, color, tickness)

  def cartoonize(self, img):
    numDownSamples = 2 # number of downscaling steps
    numBilateralFilters = 7  # number of bilateral filtering steps

    # -- STEP 1 --
    # downsample image using Gaussian pyramid
    img_color = img
    for _ in range(numDownSamples):
      img_color = cv2.pyrDown(img_color)

    # repeatedly apply small bilateral filter instead of applying
    # one large filter
    for _ in range(numBilateralFilters):
      img_color = cv2.bilateralFilter(img_color, 9, 9, 7)

    # upsample image to original size
    for _ in range(numDownSamples):
      img_color = cv2.pyrUp(img_color)

    # -- STEPS 2 and 3 --
    # convert to grayscale and apply median blur
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img_blur = cv2.medianBlur(img_gray, 7)

    # -- STEP 4 --
    # detect and enhance edges
    img_edge = cv2.adaptiveThreshold(img_blur, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 7)

    # -- STEP 5 --
    # convert back to color so that it can be bit-ANDed
    # with color image
    img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2RGB)
    return cv2.bitwise_and(img_color, img_edge)
 
  def convert_img(self, img, w=128, h=64):
    img = cv2.resize(img, (w, h))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img

  def rotate10(self, img):
    rows, cols = img.shape[0:2]
    m10 = cv2.getRotationMatrix2D((cols/2,rows/2), 10, 0.9)
    img = cv2.warpAffine(img, m10, (cols,rows))
    return img

  def bgr_hls(self, img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2HLS)

class cFace:
  def __init__(self, conf=None):
    self.model_path = conf.MODEL_PATH
    self.facedb = [[],[]]
    self.threshold = 0.4
    self.age_class = ['(0, 2)','(4, 6)','(8, 12)','(15, 20)','(25, 32)','(38, 43)','(48, 53)','(60, 100)']
    self.gender_class = ['Male', 'Female']
    self.agenet = cv2.dnn.readNetFromCaffe(
                 self.model_path+"/deploy_age.prototxt",
                 self.model_path+"/age_net.caffemodel")
    self.gendernet = cv2.dnn.readNetFromCaffe(
                    self.model_path+"/deploy_gender.prototxt",
                    self.model_path+"/gender_net.caffemodel")
    self.face_detector = cv2.CascadeClassifier(self.model_path + "/haarcascade_frontalface_default.xml")
    self.predictor = dlib.shape_predictor(self.model_path + "/shape_predictor_5_face_landmarks.dat")
    self.face_encoder = dlib.face_recognition_model_v1(self.model_path + "/dlib_face_recognition_resnet_model_v1.dat")
  
  def get_db(self):
    return self.facedb

  def init_db(self):
    self.facedb = [[], []]

  def load_db(self, filename):
    with open(filename, "rb") as f :
      self.facedb = pickle.load(f)
  
  def save_db(self, filename):
    with open(filename, "w+b") as f:
      pickle.dump(self.facedb, f)

  def train_face(self, img, face, name):
    x,y,w,h = face
    rect = dlib.rectangle(int(x), int(y), int(x + w), int(y + h))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    shape = self.predictor(gray, rect)
    face_encoding = np.array(self.face_encoder.compute_face_descriptor(img, shape, 1))

    self.facedb[0].append(name)
    self.facedb[1].append(face_encoding)
    #cv2.imwrite(self.data_path+"/{}.jpg".format(name), img[y+3:y+h-3, x+3:x+w-3]);

  def delete_face(self, name):
    ret = name in self.facedb[0]
    if ret == True:
      idx = self.facedb[0].index(name)
      #os.remove(self.data_path +"/" + name + ".jpg")
      for item in self.facedb:
        del item[idx]

    return ret

  def recognize(self, img, face):
    if len(self.facedb[0]) < 1:
      return False

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    data={"name":"Guest", "score":0}
    (x,y,w,h) = face
    rect = dlib.rectangle(int(x), int(y), int(x + w), int(y + h))
    shape = self.predictor(gray, rect)
    face_encoding = np.array(self.face_encoder.compute_face_descriptor(img, shape, 1))
    matches = []
    matches = list(np.linalg.norm(self.facedb[1] - face_encoding, axis=1))
    data["score"] = round(min(matches), 2)

    if min(matches) < self.threshold:
      data["name"] = self.facedb[0][matches.index(min(matches))]
    return data
  
  def detect(self, img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = self.face_detector.detectMultiScale(gray, 1.1, 5)
    #(x,y,w,h) = faces[0]
    return faces

  def get_ageGender(self, img, face):
    data = []

    x1, y1, w, h = face
    x2 = x1+w
    y2 = y1+h

    face_img = img[y1:y2, x1:x2].copy()
    blob = cv2.dnn.blobFromImage(face_img, scalefactor=1, size=(227, 227),
      mean=(78.4263377603, 87.7689143744, 114.895847746),
      swapRB=False, crop=False)

    # predict gender
    self.gendernet.setInput(blob)
    gender_preds = self.gendernet.forward()
    gender = self.gender_class[gender_preds[0].argmax()]

    # predict age
    self.agenet.setInput(blob)
    age_preds = self.agenet.forward()
    age = self.age_class[age_preds[0].argmax()]

    data = {"age":age, "gender":gender}

    # visualize
    #cv2.rectangle(img, (x1, y1), (x2, y2), (255,255,255), 2)
    #cv2.putText(img, "{} {}".format(gender, age), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,128,128), 2)
    return data

class cDetect:
  def __init__(self, conf=None):
    self.model_path = conf.MODEL_PATH
    self.object20_class = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus",
                    "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike",
                    "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]
    self.mobilenet = cv2.dnn.readNetFromCaffe(
                   self.model_path+"/MobileNetSSD_deploy.prototxt.txt",
                   self.model_path+"/MobileNetSSD_deploy.caffemodel")

  def detect_object(self, img):
    data = []
    (h, w) = img.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 0.007843, (300, 300), 127.5)
    self.mobilenet.setInput(blob)
    detections = self.mobilenet.forward()

    for i in np.arange(0, detections.shape[2]):
      confidence = detections[0, 0, i, 2]
      if confidence > 0.2:
        idx = int(detections[0, 0, i, 1])
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")
        data.append({"name":self.object20_class[idx], "score":confidence * 100, "position":(startX,startY,endX,endY)})
        # draw the prediction on the frame
        #label = "{}: {:.2f}%".format(self.object20_class[idx], confidence * 100)
        #cv2.rectangle(img, (startX, startY), (endX, endY), (128,0,128), 2)
        #y = startY - 15 if startY - 15 > 15 else startY + 15
        #cv2.putText(img, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,128,128), 2)
    return data

  def detect_qr(self, img):
    barcodes = pyzbar.decode(img)
    return {"data":barcodes[0].data.decode("utf-8"), "type":barcodes[0].type} if len(barcodes) > 0  else {"data":"", "type":""}

  def detect_text(self, img):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return pytesseract.image_to_string(img_rgb, lang='eng+kor', config=r'--oem 3 --psm 6')
