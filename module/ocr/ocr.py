import io
import os
from PIL import Image
from module.ocr.PPOCR_api import GetOcrApi
from utils.utils import root_path

class OCR:
   def __init__(self, exePath = ""):
      if exePath == "":
         self.exePath = os.path.join(root_path(), "PaddleOCR-json", "PaddleOCR-json.exe")
      else:
         self.exePath = exePath
      self.ocr = None

   def instance_ocr(self):
      if self.ocr is None:
         try:
            argument = {'config_path': "models/config_chinese.txt"}
            self.ocr = GetOcrApi(exePath=self.exePath, argument=argument)
         except Exception as e:
            print(e)
      
   def exit(self):
      if self.ocr is not None:
         self.ocr.exit()
         self.ocr = None
   
   def run(self, image):
      self.instance_ocr()
      if not isinstance(image, Image.Image):
         if isinstance(image, str):
            image = Image.open(os.path.abspath(image))
         else:
            image = Image.fromarray(image)
      image_stream = io.BytesIO()
      image.save(image_stream, format="PNG")
      image_bytes = image_stream.getvalue()
      original_dict = self.ocr.runBytes(image_bytes)

      return self.convert_format(original_dict)
   
   def run_list(self, img_list):
      result_list = []
      for img in img_list:

         # 合并数组 self.run(img)
         result = self.run(img)
         result_list.extend(result)
      return result_list
   
   def convert_format(self, result):
      if result['code'] != 100:
         return False
      return [[item['box'], (item['text'], item['score'])] for item in result['data']]

         
