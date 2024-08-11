
import os
from PySide6.QtCore import Signal, QThread
from cv2 import IMREAD_GRAYSCALE, imread
# from detection.detection import detect_achievement_list, detect_image_by_path
from module.ocr.ocr import OCR
from utils.image_processing import draw_covered, get_images_by_path, match_template
from utils.utils import open_file

class DetectionLightingThread(QThread):
    detectionFinished = Signal(list)

    def __init__(self, fload, achievement_list):
        super().__init__()
        self.fload = fload
        self.current_path = os.getcwd()
        self.achievement_list = achievement_list

    def process_img_list(self):
        """ 处理后的图片 """
        img_list = []
        done_hook = imread('./assets/achievements/done-hook.png', IMREAD_GRAYSCALE)
        for img_path in get_images_by_path(self.fload):
            img = imread(img_path, IMREAD_GRAYSCALE)
            match_result = match_template(img, done_hook)
            drawed_image = draw_covered(img, match_result, img.shape[0], done_hook.shape[1], 100)
            img_list.append(drawed_image)   
        return img_list

    def run(self):
        not_done_list = []
        try:
            ocr_path = os.path.join(self.current_path, "PaddleOCR-json/PaddleOCR-json.exe")
            ocr = OCR(ocr_path)
            achievement_path = os.path.join(self.current_path, "assets", "achievements", f"{self.achievement_list}.json")
            # 成就数据
            achievement_data = open_file(achievement_path)
            img_list = self.process_img_list()
            ocr_result = ocr.run_list(img_list)
            ocr_text_list = []
            for ocr_item in ocr_result:
                ocr_text = ocr_item[1][0]
                ocr_text_list.append(ocr_text)
            
            for achievement_item in achievement_data:
                objective = achievement_item.get("Objective")
                print(objective)
                if objective in ocr_text_list:
                    not_done_list.append(achievement_item)
            self.detectionFinished.emit(not_done_list)
        finally:
            ocr.exit()
            self.detectionFinished.emit(not_done_list)
