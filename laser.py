import math
import numpy as np
from transform import Matrix, mult

TOWER_POS = [-110.46551, 563.0474, 79]
TOWER_ANGLES = [0, 0, (180 + 11.1) * 2 * math.pi / 360]
WRIST_POS = [0, 0, 0]
WRIST_ANGLES = [0, 0, 0]
LASER_POS = [0, 1, 0]
SCREW_HEIGHT_PER_TURN = .15


# Matrix from top of tower center of laser
def get_wrist_matrix(angle_wrist=0):
    fixed_matrix = Matrix(pos=WRIST_POS, angles=WRIST_ANGLES)
    variable_matrix = Matrix(angles=[angle_wrist, 0, 0])
    return mult([fixed_matrix, variable_matrix])


# Rotation of infinite screw to heigth in mm
def angle_to_dist(angle_tower):
    num_turn = angle_tower / (2 * math.pi)
    dist = num_turn * SCREW_HEIGHT_PER_TURN
    return dist


# Matrix from base of tower to top of moving part(top of tower)
def get_tower_matrix(angle_tower=0):
    height = angle_to_dist(angle_tower)
    fixed_matrix = Matrix(pos=TOWER_POS, angles=TOWER_ANGLES)
    variable_matrix = Matrix(pos=[0, 0, height])
    return mult([fixed_matrix, variable_matrix])

# gets line (matrix) of line in world
def get_laser_line_in_world(angle_table=0, angle_tower=0, angle_wrist=0):
    floor_matrix = Matrix(angles=[0, 0, angle_table])
    wrist_matrix = get_wrist_matrix(angle_wrist)
    tower_matrix = get_tower_matrix(angle_tower)
    laser_matrix = mult([floor_matrix, tower_matrix, wrist_matrix])
    return laser_matrix

# transform line(matrix) to line(point,vector)
def get_laser_point_vector_in_world(angle_table=0, angle_tower=0, angle_wrist=0):
    laser_matrix_world = get_laser_line_in_world(angle_table, angle_tower, angle_wrist)
    point = laser_matrix_world.get_pos()
    unit_vector_matrix = Matrix(pos=[0, 1, 0])
    point_vector_direction = mult([laser_matrix_world, unit_vector_matrix])
    vector = point_vector_direction.get_pos() - point
    return point, vector
