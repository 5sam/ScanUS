import math
import numpy as np
from transform import Matrix, mult
import cv2
import glob

try:
    from picamera import PiCamera
except:
    1 + 1

CAMERA_MATRIX = np.array([[964.28823421, 0.0, 513.256418],
                 [0.0, 966.54236797, 372.50558502],
                 [0.0, 0.0, 1.0]])
DISTORTION_COEFF = np.array([[1.79814569e-01, -9.43894922e-01, -9.48703974e-04, 8.58610402e-04, 1.56358136e+00]])
CAMERA_POS = [10, 6, 0]
CAMERA_ANGLES = [0, 0, 0]

def normalize_2D_point(x=0,y=0):
    center = CAMERA_MATRIX[:2,2]
    x = x-center[0]
    y = y - center[1]
    return x,y

def get_red_dot_vector(x=0,y=0):
    x,y = normalize_2D_point(x,y)

    return


def get_camera_ext_matrix(angle_table=0):
    # The camera matrix should have its coordinate system with the y axis
    # pointing throught the center of the image
    angles = CAMERA_ANGLES
    floor_matrix = Matrix(angles=[0, 0, angle_table])
    cam_matrix = Matrix(pos=CAMERA_POS, angles=angles)
    result_matrix = mult([floor_matrix, cam_matrix])
    return result_matrix


def find_point_in_frame(frame, show=False):
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

    return centers[0]


def take_pictures():
    with PiCamera() as camera:
        camera.resolution = (1024,768)
        images = glob.glob('D:\_Udes\S4\Projet\ScanUS\Calibration/*.png')
        picure_index = len(images)

    while (True):
        camera.start_preview()
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
    return [[center_x, center_y]]
