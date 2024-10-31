#-*- coding:utf-8 -*-

import cv2
import numpy as np
import pyautogui
import os

def update_surrender_count(count):
    """更新投降次数的逻辑，暂时未启用。

    Args:
        count: 当前投降次数。
    """
    return count+1

# def update_surrender_count():
#     count_file = 'surrender_count.txt'
#
#     if os.path.exists(count_file):
#         with open(count_file, 'r') as f:
#             count = int(f.read())
#     else:
#         count = 0
#
#     count += 1
#
#     with open(count_file, 'w') as f:
#         f.write(str(count))
#
#     return count

def find_and_click(image_path):
    """查找并点击指定的图片。

    Args:
        image_path: 要查找的图片路径。

    Returns:
        bool: 如果找到并点击图片，返回 True；否则返回 False。
    """
    screen = pyautogui.screenshot()
    screen_np = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)

    template = cv2.imread(image_path)

    if template is None:
        print(f"警告: 无法读取图像文件: {image_path}")
        return False

    h, w, _ = template.shape
    result = cv2.matchTemplate(screen_np, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.7
    loc = np.where(result >= threshold)

    for pt in zip(*loc[::-1]):
        pyautogui.click(pt[0] + w // 2, pt[1] + h // 2)
        return True

    return False
