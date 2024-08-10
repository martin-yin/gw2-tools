import win32con
from win32 import win32api, win32gui

# 绘制target的边框
def draw_position_border(box, color=(255, 0, 255)):
    hwnd = win32gui.GetDesktopWindow()
    hwndDC = win32gui.GetWindowDC(hwnd)
    hPen = win32gui.CreatePen(win32con.PS_SOLID, 1, win32api.RGB(color[0], color[1], color[2]))
    win32gui.SelectObject(hwndDC, hPen)
    hbrush = win32gui.GetStockObject(win32con.NULL_BRUSH)
    prebrush = win32gui.SelectObject(hwndDC, hbrush)
    win32gui.Rectangle(hwndDC, box[0], box[1], box[2], box[3])
    win32gui.SelectObject(hwndDC, prebrush)
    win32gui.ReleaseDC(hwnd, hwndDC)
    win32gui.DeleteObject(hPen)
    return

# 计算两个坐获取到真实的坐标位置
def real_position(game_postion, target_postion):
    left = game_postion[0] + target_postion[0]
    top = game_postion[1] + target_postion[1]
    right = left + target_postion[2] - target_postion[0]
    bottom = top + target_postion[3] - target_postion[1]

    return (left, top, right, bottom)

# 计算坐标偏移
def offset_position(position, offset):
    left = position[0] + offset[0]
    top = position[1] + offset[1]
    right = position[2] + offset[2]
    bottom = position[3] + offset[3]

    return (left, top, right, bottom)