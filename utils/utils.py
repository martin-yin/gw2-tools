import ctypes
import json
from win32 import win32api, win32gui, win32print
import dxcam
import win32con
camera = None
hwnd = None

cnOcr = None

def get_cnOcr():
    global cnOcr
    if cnOcr is None:
        from cnocr import CnOcr
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
    width = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
    height = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
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
    
# 加载配置文件
# def load_config(file_path):
#     """
#     读取 YAML 文件并返回配置字典

#     :param file_path: YAML 文件的路径
#     :return: 包含配置信息的字典
#     """
#     with open(file_path, 'r') as file:
#         config = yaml.safe_load(file)
#     return config

# 获取游戏的dpi
def get_windows_scale():
    try:
        # 调用 Windows API 函数获取缩放比例
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        scaling_factor = user32.GetDpiForSystem()
        # 计算缩放比例
        return scaling_factor / 96.0
 
    except Exception as e:
        exit("获取 windows dpi 失败")
        return None
# 打开文件
def open_file(file_path):
    normalized_path = file_path.replace("\\", "/")
    with open(normalized_path, 'r', encoding='utf-8') as f:
        return json.load(f)