import ctypes
import json
import os
from win32 import win32gui, win32print

DESKTOPHORZRES = 118
DESKTOPVERTRES = 117

def get_real_screen_resolution():
    """ 获取 window 真实宽高"""
    hDC = win32gui.GetDC(0)
    width = win32print.GetDeviceCaps(hDC, DESKTOPHORZRES)
    height = win32print.GetDeviceCaps(hDC, DESKTOPVERTRES)
    return width, height

def open_file(file_path):
    """ 打开文件夹 """
    normalized_path = file_path.replace("\\", "/")
    with open(normalized_path, 'r', encoding='utf-8') as f:
        return json.load(f)
    
def get_windows_scale():
    try:
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        scaling_factor = user32.GetDpiForSystem()
        # 计算缩放比例
        return scaling_factor / 96.0
 
    except Exception as e:
        exit("获取 windows dpi 失败")

def root_path():
    current_path = os.path.dirname(os.path.abspath(__file__))
    root_path = os.path.dirname(current_path)
    return root_path

def join_path(dynamic_path):
    """ 拼接路径 """
    trimmed_path = dynamic_path.lstrip('/')
    parts = trimmed_path.split('/')
    full_path = os.path.join(root_path(), *parts)

    return full_path