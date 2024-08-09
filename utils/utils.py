import ctypes
from win32 import win32api, win32gui
import dxcam

camera = None
hwnd = None

# 获取激战2的窗口句柄
def get_hwnd():
    global hwnd
    if hwnd:
        return hwnd
    hwnd = win32gui.FindWindow(None, "激战2")
    if hwnd == 0:
        return None
    return hwnd

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