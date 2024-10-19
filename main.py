# -*- coding: utf-8 -*-


import cv2
import numpy as np
import pyautogui
import time
import os

def update_surrender_count():
    count_file = 'surrender_count.txt'

    if os.path.exists(count_file):
        with open(count_file, 'r') as f:
            count = int(f.read())
    else:
        count = 0

    count += 1

    with open(count_file, 'w') as f:
        f.write(str(count))

    return count

def find_and_click(image_path):
    screen = pyautogui.screenshot()
    screen_np = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
    template = cv2.imread(image_path)
    h, w, _ = template.shape
    result = cv2.matchTemplate(screen_np, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.6
    loc = np.where(result >= threshold)

    for pt in zip(*loc[::-1]):
        pyautogui.click(pt[0] + w // 2, pt[1] + h // 2)
        return True  

    return False  

def main():
    images = [
        "images/start.png",
        "images/can_throw.png",
        "images/click_to_continue.png"
    ]

    while True:
        for image in images:
            print(f"Searching: {image}")
            find_and_click(image)
            time.sleep(0.5)  # Rest a bit before trying again
            # if (image == "images/can_throw_a.png" or image == "images/can_throw_b.png") and find_and_click(image) == True:
            if (image == "images/can_throw.png") and find_and_click(image) == True:
                print("Simulating pressing the ESC key...")
                pyautogui.press('esc')  # Simulate pressing the ESC key
                find_and_click("images/throw_in_the_towel.png")
                surrender_count = update_surrender_count()
                print(f"Current surrender count: {surrender_count}")

if __name__ == "__main__":
    main()
