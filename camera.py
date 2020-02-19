import math
import numpy as np
from transform import Matrix, mult
import cv2
import glob
from picamera import PiCamera


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

def find_point_in_frame(frame,show=False):
    if show:
        cv2.namedWindow('gray', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('gray', 400, 300)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    centers = []
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(gray, 240, 255, 0)
    contours, hier = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        if cv2.contourArea(contour) > 500:
            center = getcenter(contour)
            centers += center
            if show:
                cv2.circle(frame, (int(center[0][0]), int(center[0][1])), 4, (0, 0, 255), -1)
                cv2.drawContours(frame, contour, -1, [255, 0, 0], 2)
    if show:
        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(frame, frame, mask=mask)
        cv2.imshow('gray', gray)
        cv2.imshow('frame', frame)
        cv2.imshow('mask', mask)
        print(centers)
        cv2.waitKey(0)

    return centers


def take_pictures():
    with PiCamera() as camera:
        camera.resolution = (1024,768)
        images = glob.glob('D:\_Udes\S4\Projet\ScanUS\Calibration/*.png')
        picure_index = len(images)

        while (True):
            camera.start_prewiew()
            key = input()
            camera.capture('image_' + str(picure_index) + '.png')
            picure_index += 1
            if key == 'q':
                break
        pass


def getcenter(contour):
    M = cv2.moments(contour)
    center_x = M['m10'] / M['m00']
    center_y = M['m01'] / M['m00']
    return [[center_x,center_y]]