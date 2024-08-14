import os
from time import sleep
from PySide6.QtCore import QThread, Signal
import keyboard
import pyautogui
from module.ocr.ocr import OCR

class HotkeyThread(QThread):
    finished = Signal(bool)

    def __init__(self, enable_hotkey):
        super().__init__()
        self.enable_hotkey = enable_hotkey
        self.current_path = os.getcwd()

    def find_center(self,points):
        x_coords = [point[0] for point in points]
        y_coords = [point[1] for point in points]
        
        center_x = sum(x_coords) / len(x_coords)
        center_y = sum(y_coords) / len(y_coords)
        return center_x, center_y
    
    def right_operate_destroy(self, operate = "摧毁"):
        pass
        # try:
        #     ocr = OCR()
        #     mouse_x, mouse_y = pyautogui.position()
        #     pyautogui.click(mouse_x, mouse_y, button='right')
        #     sleep(0.1)
        #     # frame = get_frame(get_frame_position(mouse_x, mouse_y, mouse_x + 220, mouse_y + 400))
        #     ocr_result = ocr.run(frame)
        #     print(ocr_result)
        #     for item in ocr_result:
        #         text = item[1][0]
        #         score = item[1][1]
        #         if text == operate and score > 0.8:
        #             position = item[0]
        #             center_x, center_y = self.find_center(position)
        #             print(center_x, center_y)
        #             pyautogui.click(mouse_x + center_x, mouse_y + center_y)
        # finally:
        #     print("操作完成")
        #     ocr.exit()

    def run(self):
        if self.enable_hotkey:
            keyboard.add_hotkey("F11", self.right_operate_destroy)
        else:
            keyboard.remove_hotkey("F11")
        self.finished.emit(self.enable_hotkey)