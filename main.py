import numpy as np
import time
import camera
import plot
from calibration import calib_camera_int, calib_camera_ext
from transform import intersect, Matrix, mult
import cv2
import math
import motor
import os
import laser
import tkinter as tk
import gui

def main_pi():
    # This code is obsolete
    # This code needs to be changed with functions from laser.py if the actual laser tower is used
    my_plot = plot.Plot(name='main plot', range=[0, 10])
    laser_p = [0, 0, 180]
    with camera.init_picamera() as cam:
        input()
        motor.start_motor()
        temp = 0;
        while (True):
            pic = camera.take_one_picture_pi(cam)
            # print(pic)
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
            # print(m, l, sep=' ')
            temp = ang
            # k = input()
            # if k == 'q':
            #    break
        motor.restart_motor()
    input()
    my_plot.close()


def main_pc():
    # this code uses pictures taken manualy
    # this is not the correct way to use the code but because of COVID-19, the setup was not obtainable
    folder = 'D:\_Udes\S4\Projet\ScanUS\Photos_boite/'
    files = os.listdir(folder)
    laser_angles = [-5, -3, -2, -1, -0.5, 0, 0.5, 1.5, 2, 3, 4]
    my_plot = plot.Plot(name='main plot', range=[0, 10])

    position_laser_ref_plaque = Matrix(pos=[259, 512, 150])
    angle_laser_cam = 11.1 * 2 * math.pi / 360 + math.atan(259 / 512)
    trans_plaque_to_cam_ref = Matrix(angles=[0, 0, angle_laser_cam])
    position_laser = mult([trans_plaque_to_cam_ref, position_laser_ref_plaque])

    for i in range(len(files)):
        filename = folder + files[i]
        img = cv2.imread(filename)
        x, y, fail = camera.find_red_dot(frame=img)

        if not fail:
            angle_table = ((i * 11.25) % 360) * 2 * math.pi / 360
            angle_laser = laser_angles[i // 32] * 2 * math.pi / 360
            p1, v1 = camera.get_red_dot_point_vector_in_world(angle_table, x, y)
            p2, v2 = laser.get_laser_point_vector_in_world(angle_table=angle_table, angle_wrist=angle_laser)
            p, error = intersect(p1, v1, p2, v2)
            my_plot.add_point(p + [error])

        if i > 11*32:
            break

    input()
    my_plot.close()


if __name__ == "__main__":
    #
    #main_pc()
    calib_camera_ext('D:\_Udes\S4\Projet\ScanUS\Calibration\Positions\92400939_675701339671843_4756966280806793216_n.png')
    #calib_camera_int()
