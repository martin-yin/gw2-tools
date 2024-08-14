# # import cv2
# # from module.ocr.ocr import OCR
# # from utils.image_processing import find_max_mactch_result, match_template

# # def find_center(points):
# #     x_coords = [point[0] for point in points]
# #     y_coords = [point[1] for point in points]
    
# #     center_x = sum(x_coords) / len(x_coords)
# #     center_y = sum(y_coords) / len(y_coords)
# #     return center_x, center_y
    

# #     # done_hook = cv2.imread('D:/gw2-tools/assets/achievements/done-hook2.png', cv2.IMREAD_GRAYSCALE)
# #     # result =  match_template(done_hook, template)

# #     # cv2.imwrite('done_hook2.png', done_hook)
# #     # cv2.imwrite('template2.png', template)
# #     # target = cv2.imread('D:/gw2-tools/test/target.png')
# #     # (x, y , max_val) = find_max_mactch_result(match_template(template, target), 0.3)
# #     # print(max_val)
# #     # print(x, y)

# #     # cv2.rectangle(template, (x, y), (x + 200, y +300), (0, 255, 0), 10)
# #     # cv2.imwrite('img2.png', template)
# #     image = cv2.imread('D:/gw2-tools/test/1.png', cv2.IMREAD_GRAYSCALE)
# #     # 全局阈值
# #     threshold_value = 127  # 阈值，可以根据图像调整
# #     max_value = 255       # 最大值
# #     ret, binary_image = cv2.threshold(image, threshold_value, max_value, cv2.THRESH_BINARY)
# #     cv2.imwrite('binary_image.png', binary_image)
# #     target = cv2.imread('D:/gw2-tools/assets/achievements/target.png', cv2.IMREAD_GRAYSCALE)
# #     # match_template(binary_image, target)

# #     # 
# #     (x, y , max_val) = find_max_mactch_result(match_template(binary_image, target), 0.3)
# #     print(max_val)
# #     print(x, y)
# #     cv2.rectangle(image, (x, y), (x + 200, y +300), (0, 255, 0), 200)
# #     # cv2.imshow('image', image)
# #     cv2.imwrite('img2.png', image)
# #     # 显示二值化后的图像
# #     # cv2.imwrite ('Binary-Image.png', binary_image)
# #     # cv2.waitKey(0)
# #     # cv2.destroyAllWindows()

# import time
# import cv2
# import numpy as np
# import pyautogui

# from module.ocr.ocr import OCR
# from utils.image_processing import match_template_with_scaling
# from utils.utils import activate_window, get_frame, get_hwnd, get_hwnw_rect


# def scrolled_to_bottom():
#     for _ in range(5):
#         pyautogui.scroll(-1)


# def main():
#     activate_window()
#     time.sleep(3)  # Allow time for the window to become active

#     # Capture initial frame and convert to grayscale
#     initial_frame = get_frame(get_hwnw_rect())
#     gray_frame = cv2.cvtColor(initial_frame, cv2.COLOR_BGR2GRAY)

#     # Read template and find best scale match
#     template_path = 'D:/gw2-tools/assets/achievements/zhaoliangneiyuesineicheng.png'
#     origin_template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
#     best_scale, _, _, top_left = match_template_with_scaling(gray_frame, origin_template)

#     # Adjust coordinates for the region of interest
#     base_offset_width = int(340 * best_scale)
#     base_offset_height = int(570 * best_scale)
#     rect = get_hwnw_rect()
#     roi_coords = (
#         rect[0] + top_left[0] - int(16 * best_scale),
#         rect[1] + top_left[1],
#         rect[0] + top_left[0] + base_offset_width,
#         rect[1] + top_left[1] + base_offset_height
#     )
#     print(f'Score: {best_scale}')
#     print(roi_coords)
#     screenshot_list = []
#     # Scroll down and capture screenshots
#     for i in range(5):
#         screenshot = get_frame(roi_coords)
#         screenshot_list.append(screenshot)
#         time.sleep(0.2)
#         scrolled_to_bottom()

#     ocr = OCR()

#     ocr_result = ocr.run_list(screenshot_list)
#     for ocr_item in ocr_result:
#         print("============")
#         print(ocr_item)
#         print("============")
# if __name__ == '__main__':
#     main()


import ctypes
# from config import Config
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
        return 1

if __name__ == '__main__':
    # config = Config()
    # print(config.get('best_scale'))

    # config.set('best_scale', 0.5)
    # config.save()
    print(get_windows_scale())


