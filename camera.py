import math
import numpy as np
from transform import Matrix, mult

FOV_V = 10
FOV_H = 10
NB_PIXELS_V = 10 / 2
NB_PIXELS_H = 10 / 2
FOCALE_H = math.atan(NB_PIXELS_H / (FOV_H / 2))
FOCALE_V = math.atan(NB_PIXELS_V / (FOV_V / 2))
CAMERA_POS = [10, 6, 0]
CAMERA_ANGLES = [0, 0, 0]


def find_line_angle(x, y):
    point = [x - NB_PIXELS_H, y - NB_PIXELS_V]
    angle_h = math.atan(point[0] / FOCALE_H)
    angle_v = math.atan(point[1] / FOCALE_V)
    return [angle_h, 0, angle_v]


def get_camera_line(angle_table=0,x=NB_PIXELS_H, y=NB_PIXELS_V):
    angles = find_line_angle(x, y)
    cam_matrix = get_camera_matrix(angle_table)
    line_matrix = Matrix(angles=angles)
    return mult([cam_matrix, line_matrix])

def get_camera_matrix(angle_table=0):
    # The camera matrix should have its coordinate system with the y axis
    # pointing throught the center of the image
    angles = CAMERA_ANGLES
    floor_matrix = Matrix(angles=[0, 0, angle_table])
    cam_matrix = Matrix(pos=CAMERA_POS, angles=angles)
    result_matrix = mult([floor_matrix, cam_matrix])
    return result_matrix
