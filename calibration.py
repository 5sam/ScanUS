import numpy as np
import cv2
import glob
import os
import camera
import transform

SQUARE_SIZE_MM = 23
CALIBRATION_IMAGES_FOLDER = 'D:\_Udes\S4\Projet\ScanUS\Calibration/*.png'
GRID_SIZE = [6, 8]
buffer = []
zooming = False


# termination criteria
def calib_camera_int(square_size_mm=SQUARE_SIZE_MM, calibration_images_folder=CALIBRATION_IMAGES_FOLDER,
                     grid_size=GRID_SIZE):
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    x = grid_size[0]
    y = grid_size[1]

    objp = np.zeros((x * y, 3), np.float32)
    objp[:, :2] = square_size_mm * np.mgrid[0:x, 0:y].T.reshape(-1, 2)
    print(objp)
    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.

    images = glob.glob(calibration_images_folder)
    i = 1
    for fname in images:

        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (x, y), None)

        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)

            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2)

            # Draw and display the corners
            # img = cv2.drawChessboardCorners(img, (x,y), corners2,ret)
            # cv2.imshow('img',img)
            # cv2.waitKey()

    # cv2.destroyAllWindows()
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    print(ret, mtx, dist, rvecs, tvecs)
    return tvecs, rvecs


def calib_camera_ext(filename_table_img):
    points_in_world = [[50, 3, 180], [-50, 3, 180], [50, 3, 80], [-50, 3, 80]]
    img_points = find_points(filename_table_img)
    img_points_vectors = []
    intersection_points = []

    for img_point in img_points:
        x = img_point[0]
        y = img_point[1]
        vec = camera.get_red_dot_vector_from_cam(x, y)
        vec[1] = -vec[1]
        vec[2] = -vec[2]
        img_points_vectors.append(vec)

    for i in range(len(img_points)):
        for j in range(len(img_points)):
            if i != j:
                intersection_points.append(
                    transform.intersect(points_in_world[i], img_points_vectors[i], points_in_world[j],
                                        img_points_vectors[j]))

    average_point = [0, 0, 0]
    error = 0
    for k in intersection_points:
        print(k)
        average_point = [average_point[i] + (k[0][i]) / len(intersection_points) for i in range(3)]
        error = error + k[1]/ len(intersection_points)
    print('Point: ', average_point)
    print('Error :', error)
    return average_point , error


def find_points(filename_table_img):
    global zooming, buffer
    original_img = cv2.imread(filename_table_img)
    img = original_img.copy()
    cv2.namedWindow('image')
    cv2.resizeWindow('image', 400, 300)
    cv2.setMouseCallback('image', event_handler)
    zoom_level = 1
    points = []
    current_point = [0, 0]

    while (True):
        cv2.imshow('image', img)
        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break

        if key == ord('z'):
            zooming = not zooming

        if key == ord('r'):
            img = original_img
            zoom_level = 1
            current_point = [0, 0]

        if zooming:
            cv2.putText(img, 'Zooming', (0, 10), cv2.FONT_HERSHEY_COMPLEX, .5, (0, 255, 0))
        else:
            cv2.putText(img, 'Zooming', (0, 10), cv2.FONT_HERSHEY_COMPLEX, .5, (0, 0, 255))

        ## Zoom
        if len(buffer) == 2:
            img = img[buffer[0][1]:buffer[1][1], buffer[0][0]:buffer[1][0]]
            current_point[0] = current_point[0] + buffer[0][0] / zoom_level
            current_point[1] = current_point[1] + buffer[0][1] / zoom_level
            buffer = []
            dim = (int(img.shape[1] * 2), int(img.shape[0] * 2))
            img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
            zoom_level *= 2

        ## Save Data
        if len(buffer) == 3:
            current_point[0] = current_point[0] + buffer[0][0] / zoom_level
            current_point[1] = current_point[1] + buffer[0][1] / zoom_level
            points.append(current_point)
            buffer = []
            img = original_img
            zoom_level = 1
            current_point = [0, 0]

    print(points)
    cv2.destroyAllWindows()
    return points


def event_handler(event, x, y, flags, param):
    global buffer, zooming
    if zooming:
        if event == cv2.EVENT_LBUTTONDOWN:
            buffer = [(x, y)]

        elif event == cv2.EVENT_LBUTTONUP:
            buffer.append((x, y))

    if event == cv2.EVENT_LBUTTONDBLCLK:
        buffer = [(x, y), None, None]
