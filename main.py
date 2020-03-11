import numpy as np
import time
import camera
import plot
from calibration import calib_camera
from transform import intersect, Matrix, mult
import cv2
import math
import motor

def main_pi():
    ## Enter your code here
    my_plot = plot.Plot(name = 'main plot',range=[0, 10])
    laser_p = [0, 0, 180]
    laser_avpef = [8, 30, 0]
    with camera.init_picamera() as cam:
        input()
        motor.start_motor()
        temp = 0;
        while (True):
            pic = camera.take_one_picture_pi(cam)
            #print(pic)
            ang = -motor.get_angle_motor()
            x, y = camera.find_red_dot(pic)
            if ang > temp:
                break
            
            floor_matrix = Matrix(angles=[0, 0, ang])
            cam_matrix = Matrix(pos=laser_p, angles=[0, 0, 0.26])
            result_matrix = mult([floor_matrix, cam_matrix])
            p2 = result_matrix.get_pos()
            v2 = result_matrix.get_vector_in_referential([0, 1, 0])
            
            p1, v1 = camera.get_red_dot_point_vector_in_world(ang, x, y)
            
            m, l = intersect(p1, v1, p2, v2)
            point = m + [l]
            my_plot.add_point(point)
            #print(m, l, sep=' ')
            temp = ang
            #k = input()
            #if k == 'q':
            #    break
        motor.restart_motor()
    input()    
    my_plot.close()

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
    main_pi()
