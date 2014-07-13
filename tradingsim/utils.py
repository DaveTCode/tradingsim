from __future__ import division
import configuration


def is_point_on_line_segment(x1, y1, x2, y2, px, py):
    left = min(x1, x2)
    right = max(x1, x2)
    top = max(y1, y2)
    bottom = min(y1, y2)

    if x2 == x1:
        return px == x2 and py < top and py > bottom
    else:
        m = (y2 - y1) / (x2 - x1)
        c = y2 - m * x2

        return py == px * m + c and py < top and py > bottom and px < right and px > left

def are_points_nearly_equal(x1, y1, x2, y2, epsilon=configuration.EPSILON):
    '''
        Given two floating point described points in R2 - return whether they're equal to within
        a sensible epsilon value.
    '''
    return abs(x1 - x2) < epsilon and abs(y1 - y2) < epsilon
