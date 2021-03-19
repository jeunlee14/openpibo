import oled.ssd1306 as ssd1306
import oled.board as board
import oled.busio as busio
import oled.digitalio as digitalio
from PIL import Image, ImageDraw, ImageFont
import PIL.ImageOps
import cv2

class cOled:
  #"font_path":"/home/pi/openpibo/lib/oled/NanumGothic.ttf",

  def __init__(self, conf=None):
    self.width = 128
    self.height = 64
    self.font_path = conf.PROC_PATH+"/KDL.ttf" # KoPub Dotum Light
    self.font_size = 10

    spi = busio.SPI(11, 10, 9)
    rst_pin = digitalio.DigitalInOut(board.D24) # any pin!
    cs_pin = digitalio.DigitalInOut(board.D8)    # any pin!
    dc_pin = digitalio.DigitalInOut(board.D23)    # any pin!

    self.oled = ssd1306.SSD1306_SPI(self.width, self.height, spi, dc_pin, rst_pin, cs_pin)
    self.font = ImageFont.truetype(self.font_path, self.font_size)
    self.image = Image.new("1", (self.width, self.height))
    self.oled.fill(0)
    self.oled.show()

  def set_font(self, filename=None, size=None):
    if filename == None:
      filename = self.font_path
    if size == None:
      size = self.font_size
    self.font = ImageFont.truetype(filename, size)

  def draw_text(self, points, text):
    draw = ImageDraw.Draw(self.image)
    draw.text(points, text, font=self.font, fill=255)

  def draw_image(self, filename):
    self.image = Image.open(filename).convert('1')

  def draw_data(self, img):
    self.image = Image.fromarray(img).convert('1')

  def draw_rectangle(self, points, fill=None):
    draw = ImageDraw.Draw(self.image)
    draw.rectangle(points, outline=1, fill=fill)

  def draw_ellipse(self, points, fill=None):
    draw = ImageDraw.Draw(self.image)
    draw.ellipse(points, outline=1, fill=fill)

  def draw_line(self, points):
    draw = ImageDraw.Draw(self.image)
    draw.line(points, fill=True)

  def invert(self):
    self.image = self.image.convert("L")
    self.image = PIL.ImageOps.invert(self.image)
    self.image = self.image.convert("1")
  
  def show(self): 
    self.oled.image(self.image)
    self.oled.show()
 
  def clear(self):
    self.image = Image.new("1", (self.width, self.height))
    self.oled.fill(0)
    self.oled.show()

  def size_check(self, filename):
    return cv2.imread(filename).shape