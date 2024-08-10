import json
from win32 import win32gui, win32print
import dxcam
from cnocr import CnOcr

DESKTOPHORZRES = 118
DESKTOPVERTRES = 117

camera = None
hwnd = None
cnOcr = None

def get_cnOcr():
    global cnOcr
    if cnOcr is None:
        cnOcr = CnOcr()
    return cnOcr

# 获取激战2的窗口句柄
def get_hwnd():
    global hwnd
    if hwnd:
        return hwnd
    hwnd = win32gui.FindWindow(None, "激战2")
    if hwnd == 0:
        return None
    return hwnd

def get_real_screen_resolution():
    hDC = win32gui.GetDC(0)
    width = win32print.GetDeviceCaps(hDC, DESKTOPHORZRES)
    height = win32print.GetDeviceCaps(hDC, DESKTOPVERTRES)
    return  width, height

def get_frame_position(letf, top, right, bottom):
    max_width, max_height = get_real_screen_resolution()

    if right > max_width:
        right = max_width
    if bottom > max_height:
        bottom = max_height
    
    return (letf, top, right, bottom)

# 获取截图
def get_frame(region):
    global camera
    if camera is None:
        camera = dxcam.create()
        
    return camera.grab(region)
    
# 打开文件
def open_file(file_path):
    normalized_path = file_path.replace("\\", "/")
    with open(normalized_path, 'r', encoding='utf-8') as f:
        return json.load(f)