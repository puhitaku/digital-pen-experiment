from numpy import matrix
from numpy.linalg import norm
from math import atan2, sin, cos

def rvec_to_tuple(mat):
    l = mat.tolist()
    return (l[0][0], l[1][0])

def lvec_to_tuple(mat):
    l = mat.tolist()
    return (l[0][0], l[0][1])

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

def vec_between_two(a, b, normalize=False, rtype=matrix):
    """Calculates the vector between a and b.

    Args:
      a (np.matrix): Point A.
      b (np.matrix): Point B.
      normalize (bool): Toggle normalization.
      rtype (type): The type of returned value.

    Returns:
      Vector between A and B. It'll be normalized if needed.

    """

    if type(a) == tuple or type(a) == list:
        _a, _b = matrix(a), matrix(b)
    elif type(a) == matrix:
        _a, _b = a, b
        
    vec = _b - _a
    n = norm(vec)
    if n > 0:
        vec_normalized = vec / n
    else:
        vec_normalized = vec

    if rtype == matrix:
        return vec_normalized if normalize else vec
    elif rtype == tuple or rtype == list:
        if normalize:
            t = vec_normalized.tolist()
        else:
            t = vec.tolist()
        return (t[0][0], t[0][1]) if rtype == tuple else [t[0][0], t[0][1]]

def get_stroke_distance(st):
    relatives = [vec_between_two(v[0], v[1], rtype=matrix) for v in zip(st[:-1], st[1:])]
    return sum( norm(v) for v in relatives )

def middle_between_two(a, b):
    return ( (a[0]+b[0])/2, (a[1]+b[1])/2 )