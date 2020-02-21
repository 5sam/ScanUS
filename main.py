import numpy as np
import time
import camera
import plot
from calibration import calib_camera
from transform import intersect
import cv2
import math

def main():
    points_3d = []
    size = 10
    ax = plot.init()
    for i in range(size):
        for j in range(size):
            for k in range(size):
                points_3d += [[i,j, k]]
            plot.plot(ax,points_3d)
            points_3d = []

    input()


    plot.plot(ax,points_3d)


if __name__ == "__main__":
    main()
