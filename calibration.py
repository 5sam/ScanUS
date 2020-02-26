import numpy as np
import cv2
import glob
import os

SQUARE_SIZE_MM = 23
CALIBRATION_IMAGES_FOLDER = 'D:\_Udes\S4\Projet\ScanUS\Calibration/*.png'
GRID_SIZE = [6, 8]


# termination criteria
def calib_camera(square_size_mm=SQUARE_SIZE_MM, calibration_images_folder=CALIBRATION_IMAGES_FOLDER,
                 grid_size=GRID_SIZE):
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    x = grid_size(0)
    y = grid_size(1)

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
