# Mock out the plotting library
# As long as test_utils is imported first
#  the plotting library will be full of no-op functions
import sys

plotting = type(sys)('plotting')
plotting.plot_points = lambda *args, **kwargs: None
plotting.draw_hull = lambda *args, **kwargs: None
plotting.draw_line = lambda *args, **kwargs: None
plotting.circle_point = lambda *args, **kwargs: None
plotting.show_plot = lambda *args, **kwargs: None
plotting.title = lambda *args, **kwargs: None
sys.modules['plotting'] = plotting


def cross(o: tuple[float, float], a: tuple[float, float], b: tuple[float, float]) -> float:
    """ Cross product of vectors OA and OB. """
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def is_point_in_polygon(point: tuple[float, float], polygon: list[tuple[float, float]]) -> bool:
    """ Check if a point is inside or on the boundary of a polygon. """
    n = len(polygon)
    wn = 0  # Winding number counter

    for i in range(n):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % n]

        if p1[1] <= point[1]:
            if p2[1] > point[1] and cross(p1, p2, point) > 0:
                wn += 1
        elif p2[1] <= point[1] and cross(p1, p2, point) < 0:
            wn -= 1

    return wn != 0


def is_convex_polygon(polygon: list[tuple[float, float]]) -> bool:
    """ Check if the given polygon is convex. """
    n = len(polygon)
    if n < 3:
        return False

    sign = None
    for i in range(n):
        o = polygon[i]
        a = polygon[(i + 1) % n]
        b = polygon[(i + 2) % n]

        cross_product = cross(o, a, b)
        current_sign = cross_product > 0

        if sign is None:
            sign = current_sign
        elif sign != current_sign:
            return False

    return True


def is_convex_hull(candidate_hull: list[tuple[float, float]], points: list[tuple[float, float]]) -> bool:
    """ Determines if `candidate_hull` is the convex hull of `points` without computing the actual convex hull. """

    # Check if all points of candidate_hull are in the original set of points
    if not set(candidate_hull).issubset(set(points)):
        return False

    # Check whether candidate_hull forms a convex polygon
    if not is_convex_polygon(candidate_hull):
        return False

    # Ensure all other points are inside or on the boundary of the candidate hull
    for point in points:
        if point not in candidate_hull and not is_point_in_polygon(point, candidate_hull):
            return False

    return True
