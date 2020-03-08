import numpy as np
import time
import camera
import plot
from calibration import calib_camera
from transform import intersect
import cv2
import math


def main_pi():
    ## Enter your code here
    cam = camera.init_picamera()
    input()
    while (True):
        pic = camera.take_one_picture_pi(cam)
        x, y = camera.find_red_dot(pic)
        p1, v1 = camera.get_red_dot_point_vector_in_world(0, x, y)
        p2 = [120, 120, 5]
        v2 = [-1, -1, 0]
        m, l = intersect(p1, v1, p2, v2)

        print(m, l, sep=' ')
        k = input()
        if k == 'q':
            break

    cam.close()


def main_pc():
    s = time.time()
    my_plot = plot.Plot(name = 'main plot',range=[0,10])
    my_plot2 = plot.Plot(name = 'inverse plot',range=[0,10])
    e = time.time()
    print(e-s)
    size = 10
    print(size)
    for i in range(size):
        for j in range(size):
            for k in range(size):
                my_plot.add_point([i, j, k,i])
                my_plot2.add_point([-i, -j, -k,k])
                #time.sleep(.01)

    input()
    my_plot.close()
    my_plot2.close()

if __name__ == "__main__":
    main_pc()
