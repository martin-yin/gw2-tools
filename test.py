import os

from cv2 import IMREAD_GRAYSCALE, imread
from module.ocr.ocr import OCR
from utils.image_processing import draw_covered, get_images_by_path, match_template
from utils.utils import open_file

def process_img_list():
    """ 处理后的图片 """
    img_list = []
    done_hook = imread('./assets/achievements/done-hook.png', IMREAD_GRAYSCALE)
    for img_path in get_images_by_path("C:/Users/martin-yin/Desktop/images"):
        img = imread(img_path, IMREAD_GRAYSCALE)
        match_result = match_template(img, done_hook)
        drawed_image = draw_covered(img, match_result, img.shape[0], done_hook.shape[1], 100)
        img_list.append(drawed_image)   
    return img_list

if __name__ == '__main__':
    current_path = os.getcwd()
    ocr_path = os.path.join(current_path, "PaddleOCR-json/PaddleOCR-json.exe")
    ocr = OCR(ocr_path)
    # 成就文件
    img_list = process_img_list()


    result = ocr.run_list(img_list)

    for ocr_item in result:
        print(ocr_item)
