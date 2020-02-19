import numpy as np
from matplotlib import pyplot as plt
import camera
from calibration import calib_camera
from transform import intersect
import cv2
import math

def main():
    frame = cv2.imread('D:\_Udes\S4\Projet\ScanUS\Images/pi_test_proche.jpg')
    camera.find_red_dot(frame)

if __name__ == "__main__":
    main()