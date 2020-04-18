import numpy as np
import math


class Matrix:
    # Angles computation order is angle_z -> angle_y -> angle_x
    def __init__(self, pos=[0, 0, 0], angles=[0, 0, 0], matrix=None):
        if matrix is None:
            pos = np.array([pos])
            matrix = self.get_angle_matrix(angles)
            matrix = np.concatenate((matrix, pos.T), axis=1)
            matrix = np.concatenate((matrix, np.array([[0, 0, 0, 1]])), axis=0)
            self.matrix = np.array(matrix)
        else:
            self.matrix = matrix

    def get_angle_matrix(self, angles=[0, 0, 0]):
        try:
            return self.matrix[0:3, 0:3]
        except:
            [tx, ty, tz] = angles
            matrix_tz = np.array([[math.cos(tz), -math.sin(tz), 0],
                                  [math.sin(tz), math.cos(tz), 0],
                                  [0, 0, 1]])
            matrix_ty = np.array([[math.cos(ty), 0, math.sin(ty)],
                                  [0, 1, 0],
                                  [-math.sin(ty), 0, math.cos(ty)]])
            matrix_tx = np.array([[1, 0, 0],
                                  [0, math.cos(tx), -math.sin(tx)],
                                  [0, math.sin(tx), math.cos(tx)]])

            rotation_matrix = np.dot(np.dot(matrix_tz, matrix_ty), matrix_tx)
            return rotation_matrix

    def get_pos(self):
        return self.matrix[:-1, 3]

    def get_vector_in_referential(self, vector):
        rotation_matrix = self.get_angle_matrix()
        return np.dot(rotation_matrix, vector)

    def __repr__(self):
        out = ''
        for line in self.matrix:
            for j in line:
                out += '%.2f' % j + '\t'
            out += '\n'
        return out


# inputs a list of matrices to multiply in that particular order
def mult(matrices):
    result = matrices[0].matrix
    for m in matrices[1:]:
        result = np.dot(result, m.matrix)
    return Matrix(matrix=result)


def intersect(point_1=np.array([0, 0, 0]), vecteur_1=np.array([0, 0, 0]), point_2=np.array([0, 0, 0]),
              vecteur_2=np.array([0, 0, 0])):
    # P1 + t1*V1 + t3*V3 = P2 + t2*V2
    vecteur_3 = np.cross(vecteur_2, vecteur_1)
    vecteur_2 = np.array([-i for i in vecteur_2])
    A = np.array([vecteur_1, vecteur_2, vecteur_3]).T
    answer = np.array([point_2[i] - point_1[i] for i in range(3)])
    B = np.array(answer)
    [t1, t2, t3] = np.dot(np.linalg.inv(A), B)
    point_3 = [t1 * vecteur_1[i] + point_1[i] for i in range(3)]
    midpoint = [point_3[i] + t3 / 2 * vecteur_3[i] for i in range(3)]
    length = abs(np.linalg.norm(vecteur_3) * t3)
    return midpoint, length
