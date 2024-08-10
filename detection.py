
import os
import cv2
import numpy as np

from utils.utils import get_cnOcr

# 图片二值化
def binarization(gray_img):
    binary = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    return binary   

# 匹配模板
def match_template(img, template):
    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    return result

# 绘制覆盖
def draw_covered(img, locs, width, height, threshold=0.5):
    threshold = 0.8
    loc = np.where(locs >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img, pt, (pt[0] + width, pt[1] + height), (0, 0, 255), -1)
        
    return img

def find_max_mactch_result(match_result, threshold=0.5):
    (min_val, max_val, min_loc, max_loc) = cv2.minMaxLoc(match_result)
    print("max_val:", max_val)
    if max_val > threshold:
        (x, y) = max_loc
        return (x, y, max_val)
    
    return None

def detect_achievement_list(img_list):    
    done_hook = cv2.imread('./assets/achievements/done-hook.png', cv2.IMREAD_GRAYSCALE)
    ocr = get_cnOcr()
    detect_list = []
    for img_path in img_list:
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        result = match_template(img, done_hook)
        drawed_image = draw_covered(img, result, img.shape[0], done_hook.shape[1], 100)
        ocr_detection_result = ocr.ocr(drawed_image)
        for item in ocr_detection_result:
            detect_list.append(item['text'])
            
    return detect_list

def detect_image_by_path(path): 
    image_list = []
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path) and (file.endswith('.png') or file.endswith('.jpg') or file.endswith('.jpeg')):
            image_list.append(file_path)
    
    return image_list


# if __name__ == '__main__':
#     list =  detect_image_by_path('C:/Users/martin-yin/Desktop/gw2-tools/detection-images')
#     result = detect_achievement_list(list)
#     print(result)

# detect_achievement('./detection-images/照亮纳约斯内层.png')   
# if __name__ == '__main__':
#     doneHook = cv2.imread('./assets/doneHook.png', cv2.IMREAD_GRAYSCALE)
#     ocr = CnOcr()  
    
#     img_list = []

#     not_done_list = [] 

#     for file in os.listdir('./detection-images'):
#         file_path = os.path.join('./detection-images', file)
#         if os.path.isfile(file_path) and file.endswith('.png'):
#             img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
#             binary = binarization(img)
#             result = match_template(binary, doneHook)
#             drawed_image = draw_covered(binary, result, img.shape[0], doneHook.shape[1], 100)
#             ocr_detection_result = ocr.ocr(drawed_image)
#             for item in ocr_detection_result:
#                 not_done_list.append(item['text'])

#     with open('./achievement-datas/照亮纳约斯内层.json', 'r', encoding='utf-8') as f:
#         data = json.load(f)
#         for item in data:
#             if item['Objective'] in not_done_list:
#                 print("\n")
#                 print("未完成的：", item['Objective'])
#                 print("观察点:", item['Game_link'])

