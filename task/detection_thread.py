
import os
import time
from PySide6.QtCore import Signal, QThread
from cv2 import  COLOR_BGR2GRAY, IMREAD_GRAYSCALE, INTER_LINEAR, cvtColor, imread, resize
from module.gw2 import gw2_instance
from utils.image_processing import draw_covered, get_images_by_path, match_template
from utils.utils import get_abs_path, get_windows_scale, open_file, root_path
from cnocr import CnOcr

class DetectionLightingThread(QThread):
    detectionFinished = Signal(object)

    def __init__(self, fload ,achievement):
        super().__init__()
        self.fload = fload
        self.achievement = achievement
        self.gw2_instance = gw2_instance
        self.ocr = CnOcr()

    def scroll_screenshot(self, position):
        screenshot_list = []
        for i in range(6):
            screenshot = self.gw2_instance.get_frame(position)
            screenshot_list.append(screenshot)
            time.sleep(0.1)
            self.gw2_instance.scroll(6)
        return screenshot_list

    def process_img_list(self, img_list):
        """ 处理后的图片 """
        window_scale = get_windows_scale()
        processed_img_list = []
        done_hook_path = os.path.join(root_path(), "assets", "achievements", "done_hook.png")
        done_hook = resize(imread(done_hook_path, IMREAD_GRAYSCALE), None, fx=window_scale, fy=window_scale, interpolation=INTER_LINEAR)
        for img in img_list:
            img = cvtColor(img, COLOR_BGR2GRAY)
            match_result = match_template(img, done_hook)
            drawed_image = draw_covered(img, match_result, img.shape[0], done_hook.shape[1], 0.8)
            processed_img_list.append(drawed_image) 
        return processed_img_list

    def ocr_img_list(self, img_list):
        """ 图片识别 """
        ocr_text_list = []
        for img in img_list:
            ocr_result = self.ocr.ocr(img)
            for item in ocr_result:
                ocr_text_list.append(item.get('text'))
        return ocr_text_list
    
    def run(self):
        """ 运行检测 """
        not_done_list = []
        img_list = []
        if self.fload != "":
            img_list = get_images_by_path(self.fload)
            if len(img_list) == 0:
                self.detectionFinished.emit({
                    "msg": "当前路径下没有找到 png jpg jepg 格式的图片",
                    "data": [],
                    "type": "error",
                })
                return
        else:
            frame_postion = self.gw2_instance.get_achievement_frame_position(self.achievement["template"])
            if frame_postion is not None:
                img_list = self.scroll_screenshot(frame_postion)
            else:
                self.detectionFinished.emit({
                    "msg": "没有在当前游戏窗口中找到成就的位置",
                    "data": [],
                    "type": "error",
                })
                return 
        try:
            achievement_data = open_file(get_abs_path(self.achievement['data_path']))
            # 获取成就数据
            processed_img_list = self.process_img_list(img_list)
            ocr_text_list = self.ocr_img_list(processed_img_list)
            for achievement_item in achievement_data:
                objective = achievement_item.get("Objective")
                if objective in ocr_text_list:
                    not_done_list.append(achievement_item)

            self.detectionFinished.emit({
                "msg":"检测完成……",
                "data": not_done_list,
                "type": "success",
            })

        except Exception as e:
            self.detectionFinished.emit({
                "msg":"检测失败……请稍后再试，不行请咨询作者",
                "data": [],
                "type": "error",
            })