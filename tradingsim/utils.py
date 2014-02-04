from __future__ import division


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
