import ctypes
import json
import os
from win32 import win32gui, win32print
import dxcam

DESKTOPHORZRES = 118
DESKTOPVERTRES = 117

camera = None
hwnd = None

# 获取激战2的窗口句柄
# def get_hwnd():
#     global hwnd
#     if hwnd:
#         return hwnd
#     hwnd = win32gui.FindWindow(None, "激战2")
#     if hwnd == 0:
#         return None
#     return hwnd

# def get_hwnd_rect():
#     hwnd = get_hwnd()
#     if hwnd is None:
#         return None
#     return win32gui.GetWindowRect(hwnd)

def get_real_screen_resolution():
    """ 获取 window 真实宽高"""
    hDC = win32gui.GetDC(0)
    width = win32print.GetDeviceCaps(hDC, DESKTOPHORZRES)
    height = win32print.GetDeviceCaps(hDC, DESKTOPVERTRES)
    return width, height


# def activate_window(): 
#     hwnd = get_hwnd()
#     if hwnd is None:
#         return False
#     win32gui.SetForegroundWindow(hwnd)
#     return True

# def get_frame_position(letf, top, right, bottom):
#     max_width, max_height = get_real_screen_resolution()

#     if right > max_width:
#         right = max_width
#     if bottom > max_height:
#         bottom = max_height
    
#     return (letf, top, right, bottom)

# 获取截图
# def get_frame(region):
#     global camera
#     if camera is None:
#         camera = dxcam.create()
        
#     return camera.grab(region)
    
def open_file(file_path):
    """ 打开文件夹 """
    normalized_path = file_path.replace("\\", "/")
    with open(normalized_path, 'r', encoding='utf-8') as f:
        return json.load(f)
    
def root_path():
    current_path = os.path.dirname(os.path.abspath(__file__))
    root_path = os.path.dirname(current_path)
    return root_path

def get_windows_scale():
    try:
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        scaling_factor = user32.GetDpiForSystem()
        # 计算缩放比例
        return scaling_factor / 96.0
 
    except Exception as e:
        exit("获取 windows dpi 失败")

def join_path(dynamic_path):
    """ 拼接路径 """
    trimmed_path = dynamic_path.lstrip('/')
    parts = trimmed_path.split('/')
    full_path = os.path.join(root_path(), *parts)

    return full_path