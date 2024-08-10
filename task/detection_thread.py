
import os
from PySide6.QtCore import Signal, QThread

from detection import detect_achievement_list, detect_image_by_path
from utils.utils import open_file

class DetectionLightingThread(QThread):
    detectionFinished = Signal(list)

    def __init__(self, fload, achievement_list):
        super().__init__()
        self.fload = fload
        self.achievement_list = achievement_list

    def run(self):
        not_done_list = []
        try:
            current_path = os.getcwd()
            achievement_list_path = os.path.join(current_path, "assets", "achievements", f"{self.achievement_list}.json")
            achievement_list = open_file(achievement_list_path)
            img_list = detect_image_by_path(self.fload)
            ocr_list = detect_achievement_list(img_list)
            for achievement_item in achievement_list:
                objective = achievement_item.get('Objective')
                if objective in ocr_list:
                    not_done_list.append(achievement_item)
        finally:
            self.detectionFinished.emit(not_done_list)
