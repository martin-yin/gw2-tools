import time
import cv2
import keyboard
import pyautogui
from detection import binarization, find_max_mactch_result, match_template
from utils.utils import get_frame

# 自动销毁
def right_operate_destroy():
    mouse_x, mouse_y = pyautogui.position()
    pyautogui.click(mouse_x, mouse_y, button='right')
    time.sleep(0.1)
    frame = get_frame((mouse_x, mouse_y, mouse_x + 220, mouse_y + 400))
    gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    binary_img = binarization(gray_img)
    target = cv2.imread('./assets/destroy.png', cv2.IMREAD_GRAYSCALE)
    result = match_template(binary_img, target)
    macth_result = find_max_mactch_result(result)
    if macth_result is not None and macth_result[2] > 0.5:
        pyautogui.click(mouse_x + macth_result[0], mouse_y + macth_result[1])

# 触发自动出售
def right_operate_sell():
    mouse_x, mouse_y = pyautogui.position()
    pyautogui.click(mouse_x, mouse_y, button='right')
    time.sleep(0.1)
    frame = get_frame((mouse_x, mouse_y, mouse_x + 220, mouse_y + 400))
    cv2.imwrite("frame.png", frame)
    gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    binary_img = binarization(gray_img)
    # cv2.imwrite('binary_img.png', binary_img)
    target = cv2.imread('./assets//sell.png', cv2.IMREAD_GRAYSCALE)
    result = match_template(binary_img, target)
    macth_result = find_max_mactch_result(result)
    if macth_result is not None and macth_result[2] > 0.5:
        pyautogui.click(mouse_x + macth_result[0], mouse_y + macth_result[1])

def on_trigger_destroy():
    right_operate_destroy()
    
