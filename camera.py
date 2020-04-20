from math import pi
import numpy as np
from transform import Matrix, mult
import cv2
import time
import glob

try:
    from picamera import PiCamera
except:
    pass

# mtx from calib_camera_int
CAMERA_MATRIX = np.array([[964.28823421, 0.0, 513.256418],
                          [0.0, 966.54236797, 372.50558502],
                          [0.0, 0.0, 1.0]])
# dst from calib_camera_int
DISTORTION_COEFF = np.array([[1.79814569e-01, -9.43894922e-01, -9.48703974e-04, 8.58610402e-04, 1.56358136e+00]])

# output of calib_camera_ext
CAMERA_POS = [-14.56, 352.77, 103.44]
CAMERA_ANGLES = [0, 0, pi]


def normalize_2D_point(x=0, y=0):
    center = CAMERA_MATRIX[:2, 2]
    x = x - center[0]
    y = y - center[1]
    return x, y

# transform image point to vector using intrinsic parameters
def get_red_dot_vector_from_cam(x=0, y=0):
    # x,y = normalize_2D_point(x,y)
    # A = RB
    # A is position in image (in pixels)
    # R is camera matrix (units in pixels)
    # B is position in real (units in mm)
    # so inv(R)*A = B

    A = np.array([x, y, 1])
    R = CAMERA_MATRIX
    inv_R = np.linalg.inv(R)
    B = np.dot(inv_R, A)
    # the next line is to represent the vector given from the camera
    # in the proper coordinate  system
    v_red_dot_cam_ref = [B[i] for i in [0, 2, 1]]
    v_red_dot_cam_ref[2] = -v_red_dot_cam_ref[2]
    return v_red_dot_cam_ref

# get the line(point,vector) of the line from camera to point in the world
def get_red_dot_point_vector_in_world(angle_table=0, x_image=0, y_image=0, cam_pos=CAMERA_POS,
                                      cam_angles=CAMERA_ANGLES):
    m_cam_ext = get_camera_ext_matrix(angle_table, cam_pos, cam_angles)
    point = m_cam_ext.get_pos()
    v_red_dot_cam_ref = get_red_dot_vector_from_cam(x_image, y_image)
    m_red_dot_cam_ref = Matrix(pos=v_red_dot_cam_ref)
    m_red_dot_world_ref = mult([m_cam_ext, m_red_dot_cam_ref])
    p_red_dot_world_ref = m_red_dot_world_ref.get_pos()
    p_cam_world_ref = m_cam_ext.get_pos()
    vector = list(p_red_dot_world_ref - p_cam_world_ref)
    return point, vector

# find the position of the camera in world
def get_camera_ext_matrix(angle_table=0, cam_pos=CAMERA_POS, cam_angles=CAMERA_ANGLES):
    # The camera ext matrix should have its coordinate system with
    # the y axis pointing through the center of the image
    floor_matrix = Matrix(angles=[0, 0, angle_table])
    cam_matrix = Matrix(pos=cam_pos, angles=cam_angles)
    result_matrix = mult([floor_matrix, cam_matrix])
    return result_matrix


# locates the center on the brigthest blob
def find_red_dot(frame, show=False):
    if len(frame) < 1:
        return 0, 0, True

    start = time.time()
    if show:
        cv2.namedWindow('gray', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('gray', 400, 300)
        cv2.namedWindow('mask', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('mask', 400, 300)
        cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('frame', 400, 300)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    centers = []
    mask = cv2.inRange(gray, 20, 255, 0)
    contours, hier = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        # print(cv2.contourArea(contour))
        if cv2.contourArea(contour) > 5 and cv2.contourArea(contour) < 100:
            center = getcenter(contour)
            centers += center
            if show:
                cv2.circle(frame, (int(center[0][0]), int(center[0][1])), 4, (0, 0, 255), -1)
                cv2.drawContours(frame, contour, -1, [255, 0, 0], 2)
    end = time.time()
    # print('time to find red dot : ', end - start)
    if show:
        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(frame, frame, mask=mask)
        cv2.imshow('gray', gray)
        cv2.imshow('frame', frame)
        cv2.imshow('mask', mask)
        print(centers)
        cv2.waitKey(0)
    if centers:
        return centers[0][0], centers[0][1], False
    else:
        return 0, 0, True

# initiate the picamera
def init_picamera():
    camera = PiCamera()
    camera.resolution = (1024, 768)
    camera.iso = 100  # entre 100 et 800 (high light to low light)
    # wait for automatic gain control to settle
    time.sleep(2)
    camera.shutter_speed = camera.exposure_speed
    camera.exposure_mode = 'off'
    gain = camera.awb_gains
    camera.awb_mode = 'off'
    camera.awb_gains = gain
    camera.start_preview()
    return camera

# self explanatory
def take_one_picture_pi(camera):
    image = np.empty((768, 1024, 3), dtype=np.uint8)
    camera.capture(image, 'bgr')
    image = image.reshape((768, 1024, 3))
    return image

# takes multiple pictures using enter to take picture and q to exit
# names pictures with index and put in specified folder
def take_pictures_pi():
    with PiCamera() as camera:
        camera.resolution = (1024, 768)
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


# transform contour to x,y center of contour
def getcenter(contour):
    M = cv2.moments(contour)
    center_x = M['m10'] / M['m00']
    center_y = M['m01'] / M['m00']
    return [[center_x, center_y]]
