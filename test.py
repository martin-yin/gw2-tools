from cv2 import IMREAD_GRAYSCALE, THRESH_BINARY, imread, imwrite, threshold


def binarize_image(path):
    img = imread(path, IMREAD_GRAYSCALE)
    threshold_value = 127  
    max_value = 255     
    ret, binary_image = threshold(img, threshold_value, max_value, THRESH_BINARY)
    return ret, binary_image

if __name__ == '__main__':
    _, result = binarize_image('D://gw2-tools//20240814235531.png')

    imwrite('./2.png', result)