import unittest
import numpy as np
import camera
import cv2

test_image_good = 'D:\_Udes\S4\Projet\ScanUS\Photos_boite\photo_0.png'
test_image_bad = 'D:\_Udes\S4\Projet\ScanUS\imagetestjuan.jpg'


class TestCamera(unittest.TestCase):

    def test_find_red_dot(self):
        frame = []
        np.testing.assert_allclose(camera.find_red_dot(frame), [0,0, True])

        frame = cv2.imread(test_image_good)
        ## actual value obtained with paint
        np.testing.assert_allclose(camera.find_red_dot(frame), [462, 637, False], atol=.5)

        frame = cv2.imread(test_image_bad)
        ## actual value obtained with paint
        np.testing.assert_allclose(camera.find_red_dot(frame), [0,0,True])

    def test_get_camera_matrix(self):
        np.testing.assert_allclose(camera.get_camera_matrix())