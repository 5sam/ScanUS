import numpy as np
import time
import camera
import plot
from calibration import calib_camera
from transform import intersect
import cv2
import math
import multiprocessing


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
    m = multiprocessing.Manager()
    mutex = multiprocessing.Lock()
    points = m.list()
    t = multiprocessing.Process(target=plot.plot,args=(points,mutex))
    t.start()
    size = 10

    time.sleep(1)
    print(size)
    for i in range(size):
        for j in range(size):
            for k in range(size):
                mutex.acquire()
                points += [[i,j,k]]
                mutex.release()
            time.sleep(0.01)

    input()
    print(points)
    t.terminate()

if __name__ == "__main__":
    main_pc()
