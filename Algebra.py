from numpy import matrix
from math import atan2, sin, cos

def angle_from_vector(vec):
    return atan2(vec.tolist()[1][0], vec.tolist()[0][0])

def angle_from_tuple(vec):
    return atan2(vec[1], vec[0])

def get_rot_matrix(t):
    mat = matrix([[cos(t), -sin(t)],
                  [sin(t),  cos(t)]])
    return mat

def shift_position(a, b):
    return tuple(sum(x) for x in zip(a, b))

def vec_between_two_pts(a, b):
    return matrix()