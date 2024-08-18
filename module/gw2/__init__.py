
import time
from cv2 import COLOR_BGR2GRAY, IMREAD_GRAYSCALE, INTER_LINEAR, TM_CCOEFF_NORMED, cvtColor, imread, matchTemplate, minMaxLoc, resize
import pyautogui
from win32 import win32gui
import dxcam
from utils.utils import get_windows_scale, get_abs_path

class Gw2:
    def __init__(self):
        self.hwnd = None
        self.camera = dxcam.create()

    def get_hwnd(self):
        """ 获取窗口句柄 """
        if self.hwnd is None or self.hwnd == 0:
            self.hwnd = win32gui.FindWindow(None, "激战2")
        return self.hwnd
    
    def activate_window(self): 
        """ 窗口前置 """
        if self.hwnd is None:
            return False
        win32gui.SetForegroundWindow(self.hwnd)

    def get_hwnd_rect(self):
        """ 获取窗口的位置 """
        if self.hwnd is None:
            return None
        return win32gui.GetWindowRect(self.hwnd)

    def get_safe_frame_position(self, position):
        """ 获取最大并且安全的窗口位置，防止超出屏幕，并返回够截图的位置 """
        _, _, max_width, max_height = self.get_hwnd_rect()
        letf, top, right, bottom = position

        if right > max_width:
            right = max_width
        if bottom > max_height:
            bottom = max_height
        return (letf, top, right, bottom)

    def get_frame(self, position):
        """ 获取指定位置的截图 """
        if self.hwnd is None:
            return None
        max_rect = self.get_safe_frame_position(position)
        return self.camera.grab(max_rect)
  
    def get_achievement_frame_position(self, achievement):
        """ 通过成就名称找到该成就合适的截图位置"""
        self.activate_window()
        time.sleep(1)
        window_scale = get_windows_scale()
        template = imread(get_abs_path(achievement), IMREAD_GRAYSCALE)
        scaled_template = resize(template, None, fx=window_scale, fy=window_scale, interpolation=INTER_LINEAR)
        initial_frame = self.get_frame(self.get_hwnd_rect())
        gray_frame = cvtColor(initial_frame, COLOR_BGR2GRAY)
        res = matchTemplate(gray_frame, scaled_template, TM_CCOEFF_NORMED)
        _, score, _, top_left = minMaxLoc(res)

        if score > 0.8:
            base_offset_width = int(340 * window_scale)
            base_offset_height = int(570 * window_scale)
            rect = self.get_hwnd_rect()
            letf = rect[0] + top_left[0] - int(16 * window_scale)
            top = rect[1] + top_left[1]
            right = rect[0] + top_left[0] + base_offset_width
            bottom = rect[1] + top_left[1] + base_offset_height
            # 偏移鼠标位置防止遮挡
            pyautogui.moveTo(right, top)
            roi_coords = (
                letf,
                top,
                right,
                bottom
            )
            return roi_coords
        return None

    def scroll(self, frequency = 5,  type = -1):
        """ 滚动窗口 """
        for i in range(frequency):
            pyautogui.scroll(type)

gw2_instance = Gw2()
