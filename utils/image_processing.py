import os
from cv2 import matchTemplate, TM_CCOEFF_NORMED,  rectangle, minMaxLoc, imread, IMREAD_GRAYSCALE
from numpy import where

def match_template(img, template):
    """ 匹配模板 """
    result = matchTemplate(img, template, TM_CCOEFF_NORMED)
    return result

def draw_covered(img, locs, width, height, threshold=0.8):
    """ 绘制覆盖 """
    loc = where(locs >= threshold)
    for pt in zip(*loc[::-1]):
       rectangle(img, pt, (pt[0] + width, pt[1] + height), (0, 0, 255), -1)
        
    return img

def find_max_mactch_result(match_result, threshold=0.8):
    """ 通过 path 抓取图片 """
    (min_val, max_val, min_loc, max_loc) = minMaxLoc(match_result)
    print("max_val:", max_val)
    if max_val > threshold:
        (x, y) = max_loc
        return (x, y, max_val)
    return None

def get_images_by_path(path): 
    """ 通过 path 抓取图片 """
    image_list = []
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path) and (file.endswith('.png') or file.endswith('.jpg') or file.endswith('.jpeg')):
            image_list.append(file_path)
    
    return image_list