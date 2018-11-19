import cv2
import math
import numpy as np

def display_image(win_name, image):
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(win_name, 800, 800)
    cv2.imshow(win_name, image)
    cv2.waitKey(0)