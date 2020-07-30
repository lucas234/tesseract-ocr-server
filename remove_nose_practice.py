# auther：Liul8
# date：2020/7/29 13:56
# tools：PyCharm
# Python：3.7.7
import cv2
import numpy as np
from PIL import Image
import pytesseract


def morphology(img):
    kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 14))  # 腐蚀矩阵
    iFushi = cv2.morphologyEx(img, cv2.MORPH_DILATE, kernel1)  # 对文字腐蚀运算
    # cv2.imshow('fushi', iFushi)
    # cv2.imwrite('7291.jpg', iFushi)

    kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 40))  # 膨胀矩阵
    iPengzhang = cv2.morphologyEx(iFushi, cv2.MORPH_ERODE, kernel2)  # 对背景进行膨胀运算

    # 背景图和二分图相减-->得到文字
    jian = np.abs(iPengzhang - img)
    # cv2.imshow("jian", jian)
    cv2.imwrite('morphology.jpg', jian)

    # kernel3 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 6))  # 膨胀
    # iWenzi = cv2.morphologyEx(jian, cv2.MORPH_DILATE, kernel3)  # 对文字进行膨胀运算
    # cv2.imshow('wenzi', iWenzi)
    # cv2.imwrite('7294.jpg', iWenzi)


def black_and_white_conversion(image_):
    """图片黑白颜色反转"""
    img = cv2.imread(image_, 1)  # 读取一张图片，彩色
    cha = img.shape
    height, width, deep = cha
    dst = np.zeros((height, width, 3), np.uint8)
    for i in range(height):  # 色彩反转
        for j in range(width):
            b, g, r = img[i, j]
            dst[i, j] = (255 - b, 255 - g, 255 - r)
    # cv2.imshow('img', img)
    cv2.imwrite('black_and_white_conversion.jpg', dst)


def remove_nose(picture_name, threshold=200):
    """去噪，通过修改阈值来观察效果"""
    table = [0 if _ < threshold else 1 for _ in range(256)]
    im = Image.open(picture_name)
    imgry = im.convert('L')
    out = imgry.point(table, '1')
    out.save("remove_nose.jpg")
    # text = pytesseract.image_to_string(out)
    return out

image = cv2.imread('./images/validate_code.jpg')
morphology(image)
remove_nose("morphology.jpg")
# black_and_white_conversion("remove_nose.jpg")
print(pytesseract.image_to_string("remove_nose.jpg"))
