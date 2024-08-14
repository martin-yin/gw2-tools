
import os
import time
from PySide6.QtCore import Signal, QThread
import cv2
from cv2 import IMREAD_GRAYSCALE, INTER_LINEAR, TM_CCOEFF_NORMED, imread, matchTemplate, minMaxLoc, resize
from module.ocr.ocr import OCR
from utils.image_processing import draw_covered, get_images_by_path, match_template
from utils.utils import activate_window, get_frame, get_hwnw_rect, open_file, root_path

# 1. 接收到要处理的成就类型
# 2. 读取对应的成就图片
# 3. 计算匹配比例系数（如果配置中有从配置中抓取）
# 4. 图片截图
# 5. ocr 识别图片

class DetectionLightingThread(QThread):
    detectionFinished = Signal(list)

    def __init__(self, detection_type ,achievement):
        super().__init__()

        self.detection_type = detection_type
        self.achievement = achievement

    def process_img_list(self, img_list):
        """ 处理后的图片 """
        img_list = []
        # done_hook_path = os.path.join(root_path(), "assets", "achievements", "done_hook.png")
        # done_hook = imread(done_hook_path, IMREAD_GRAYSCALE)
        # for img_path in img_list:
        #     img = imread(img_path, IMREAD_GRAYSCALE)
        #     match_result = match_template(img, done_hook)
        #     drawed_image = draw_covered(img, match_result, img.shape[0], done_hook.shape[1], 0.7)
        #     cv2.imwrite(f"{time.time()}.png", drawed_image)
        #     img_list.append(drawed_image)   
        # return img_list

    def scroll_screenshot(self):
        activate_window()
        time.sleep(1)
        template = imread(self.achievement.template, IMREAD_GRAYSCALE)
        scaled_template = resize(template, None, fx=1.5, fy=1.5, interpolation=INTER_LINEAR)
        initial_frame = get_frame(get_hwnw_rect())
        gray_frame = cv2.cvtColor(initial_frame, cv2.COLOR_BGR2GRAY)
        res = matchTemplate(gray_frame, scaled_template, TM_CCOEFF_NORMED)
        _, score, _, top_left = minMaxLoc(res)
        if score > 0.8:
            print(f"Achievement {self.achievement.name} found at {top_left}")

    def run(self):
        not_done_list = []
        img_list = []
        if self.detection_type == "auto":
            print("执行脚本自动抓取")


        if self.detection_type == "img":
            print("执行脚抓取图片检测")
        # try:
        #     ocr = OCR()
        #     achievement_path = os.path.join(root_path(), "assets", "achievements", f"{self.achievement_list}.json")
        #     achievement_data = open_file(achievement_path)
            
        #     img_list = self.process_img_list(img_list=self.get_images_by_path())
        #     ocr_result = ocr.run_list(img_list)
        #     ocr_text_list = []
        #     for ocr_item in ocr_result:
        #         ocr_text = ocr_item[1][0]
        #         ocr_text_list.append(ocr_text)
        #         print(f"OCR Result: {ocr_text}")
                
        #     for achievement_item in achievement_data:
        #         objective = achievement_item.get("Objective")
        #         if objective in ocr_text_list:
        #             not_done_list.append(achievement_item)
        #     self.detectionFinished.emit(not_done_list)
        # finally:
        #     ocr.exit()
        #     self.detectionFinished.emit(not_done_list)
