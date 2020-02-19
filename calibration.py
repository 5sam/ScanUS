import numpy as np
import cv2
import glob
import os


# termination criteria
def calib_camera():
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    objp = np.zeros((6 * 8, 3), np.float32)
    objp[:, :2] = 23 * np.mgrid[0:6, 0:8].T.reshape(-1, 2)  # squares on calibration grid where 23 mm
    print(objp)
    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.

    images = glob.glob('D:\_Udes\S4\Projet\ScanUS\Calibration/*.png')
    i = 1
    for fname in images:

        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (6, 8), None)

        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)

            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2)

            # Draw and display the corners
            # img = cv2.drawChessboardCorners(img, (6,8), corners2,ret)
            # cv2.imshow('img',img)
            # cv2.waitKey()

    # cv2.destroyAllWindows()
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    print(ret, mtx, dist, rvecs, tvecs)
