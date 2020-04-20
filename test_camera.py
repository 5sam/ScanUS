import unittest
import numpy as np
import camera
import cv2
from math import pi
import transform

test_image_good = 'D:\_Udes\S4\Projet\ScanUS\Photos_boite\photo_0.png'
test_image_bad = 'D:\_Udes\S4\Projet\ScanUS\imagetestjuan.jpg'


class TestCamera(unittest.TestCase):

    def test_find_red_dot(self):
        frame = []
        np.testing.assert_allclose(camera.find_red_dot(frame), [0, 0, True])

        frame = cv2.imread(test_image_good)
        ## actual value obtained with paint
        np.testing.assert_allclose(camera.find_red_dot(frame), [462, 637, False], atol=.5)

        frame = cv2.imread(test_image_bad)
        ## actual value obtained with paint
        np.testing.assert_allclose(camera.find_red_dot(frame), [0, 0, True])

    def test_get_camera_matrix(self):
        CAM_POS = [10, -1, 32]
        CAM_ANGLES = [0, 0, 0]
        TABLE_ANGLE = -pi/2

        EXPECTED_POS = [-1, -10, 32]
        np.testing.assert_allclose(
            camera.get_camera_ext_matrix(angle_table=TABLE_ANGLE, cam_pos=CAM_POS, cam_angles=CAM_ANGLES).get_pos(),
            EXPECTED_POS)

        EXPECTED_ANGLE_MATRIX = [[0, 1, 0],
                                 [-1, 0, 0],
                                 [0, 0, 1]]
        np.testing.assert_allclose(
            camera.get_camera_ext_matrix(angle_table=TABLE_ANGLE, cam_pos=CAM_POS,
                                         cam_angles=CAM_ANGLES).get_angle_matrix(),
            EXPECTED_ANGLE_MATRIX, atol=0.01)
