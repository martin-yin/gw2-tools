from win32 import win32api, win32gui
import win32con

# 按键事件
def map_virtual_key(vk_code):
    return win32api.MapVirtualKey(vk_code, 0)

# 发送键盘事件
def key_down_up(hwnd, vk_code):
    scan_code = map_virtual_key(vk_code)

    lParam_KeyDown = (1 << 0) | (scan_code << 16) | (0 << 24) | (0 << 29) | (0 << 30) | (0 << 31)
    lParam_KeyUp = (1 << 0) | (scan_code << 16) | (0 << 24) | (0 << 29) | (1 << 30) | (1 << 31)
    win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, vk_code, lParam_KeyDown)
    win32gui.PostMessage(hwnd, win32con.WM_KEYUP, vk_code,lParam_KeyUp)

def key_down(hwnd, vk_code):
    scan_code = map_virtual_key(vk_code)
    lParam_KeyDown = (1 << 0) | (scan_code << 16) | (0 << 24) | (0 << 29) | (0 << 30) | (0 << 31)
    win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, vk_code, lParam_KeyDown)

def key_up(hwnd, vk_code):
    scan_code = map_virtual_key(vk_code)
    lParam_KeyUp = (1 << 0) | (scan_code << 16) | (0 << 24) | (0 << 29) | (1 << 30) | (1 << 31)
    win32gui.PostMessage(hwnd, win32con.WM_KEYUP, vk_code,lParam_KeyUp)

# 获取当前鼠标的位置
def get_mouse_position():
    return win32api.GetCursorPos()

# 移动鼠标到指定位置
def move_mouse(x, y):
    win32api.SetCursorPos((x, y))
    
# 鼠标左键按下
def mouse_left_click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

# 鼠标右键按下
def mouse_right_click():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)