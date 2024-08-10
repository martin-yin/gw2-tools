from time import sleep
from numpy import mean
import pyautogui
from utils.utils import get_cnOcr, get_frame, get_frame_position

# 自动右键操作
def right_operate_destroy(operate = "摧毁"):
    try:
        mouse_x, mouse_y = pyautogui.position()
        pyautogui.click(mouse_x, mouse_y, button='right')
        sleep(0.1)
        frame = get_frame(get_frame_position(mouse_x, mouse_y, mouse_x + 220, mouse_y + 400))
        ocr = get_cnOcr()
        ocr_list = ocr.ocr(frame, cls=True)
        for item in ocr_list:
            position = item.get('position')
            center_x = mean(position[:, 0])
            center_y = mean(position[:, 1])
            if item.get('text') == operate and item.get('score') > 0.9:
                pyautogui.click(mouse_x + center_x, mouse_y + center_y)
    finally:
        print("操作完成")