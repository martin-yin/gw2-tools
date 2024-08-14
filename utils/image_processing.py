import os
from cv2 import matchTemplate, TM_CCOEFF_NORMED, threshold, rectangle, minMaxLoc, imread, IMREAD_GRAYSCALE, resize, matchTemplate, INTER_LINEAR, THRESH_BINARY
from numpy import where, arange

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
            image_list.append(imread(file_path, IMREAD_GRAYSCALE))
    
    return image_list

def match_template_with_scaling(img, template, scaling_step=0.1, min_scale=1.0, max_scale=2.0):
    """ 获取模板匹配结果，并进行缩放 """
    best_score = float("-inf")
    best_scale = 1
    best_matching_scale = None
    best_top_left = (0, 0)
    
    for scale in arange(min_scale, max_scale + scaling_step, scaling_step):
        scaled_template = resize(template, None, fx=scale, fy=scale, interpolation=INTER_LINEAR)
        if scaled_template.shape[0] > img.shape[0] or scaled_template.shape[1] > img.shape[1]:
            continue
        res = matchTemplate(img, scaled_template, TM_CCOEFF_NORMED)
        _, score, _, top_left = minMaxLoc(res)
        if score > best_score: 
            best_score = score
            best_scale = scale
            best_matching_scale = scaled_template
            best_top_left = top_left
    return best_scale, best_matching_scale, best_score, best_top_left

# 图片二值化
def binarize_image(path):
    img = imread(path, IMREAD_GRAYSCALE)
    threshold_value = 127  
    max_value = 255     
    ret, binary_image = threshold(img, threshold_value, max_value, THRESH_BINARY)