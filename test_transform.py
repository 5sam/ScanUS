import unittest
import numpy as np
import cv2
from math import pi
from transform import Matrix, mult, intersect


class Test_Transform(unittest.TestCase):

    def test_Matrix(self):
        # expected answers where hand calculated
        pos = [1, 2, 3]
        angles = [0, 0, pi / 2]
        expected_angles = [[0, -1, 0],
                           [1, 0, 0],
                           [0, 0, 1]]

        np.testing.assert_allclose(Matrix(pos=pos, angles=angles).get_pos(), pos)
        np.testing.assert_allclose(Matrix(pos=pos, angles=angles).get_angle_matrix(), expected_angles, atol=0.01)

    def test_mult(self):
        # expected answers where hand calculated
        ma = Matrix(pos=[1, 2, 3], angles=[0, -pi / 2, 0])
        mb = Matrix(pos=[0, 0, 0], angles=[0, 0, pi / 2])

        expected_a_b = np.array([[0, 0, -1, 1],
                                 [1, 0, 0, 2],
                                 [0, -1, 0, 3],
                                 [0, 0, 0, 1]])

        expected_b_a = np.array([[0, -1, 0, -2],
                                 [0, 0, -1, 1],
                                 [1, 0, 0, 3],
                                 [0, 0, 0, 1]])


        np.testing.assert_allclose(mult([ma, mb]).matrix, expected_a_b, atol=0.01)
        np.testing.assert_allclose(mult([mb, ma]).matrix, expected_b_a, atol=0.01)

    def test_intersect(self):
        # expected answers where calculated with geogebra
        p1 = [1,2,3]
        p2 = [4,5,6]
        v1 = [-7,-8,9]
        v2 = [-1,2,-3]
        expected = [[3.02,6.09,1.1],3.66]

        np.testing.assert_allclose(intersect(p1,v1,p2,v2)[0],expected[0],atol=0.01)
        np.testing.assert_allclose(intersect(p1,v1,p2,v2)[1],expected[1],atol=0.01)
