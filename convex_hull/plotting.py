import matplotlib.pyplot as plt


def plot_points(points: list[tuple[float, float]], **kwargs):
    if 'c' not in kwargs:
        kwargs['c'] = 'k'

    xx, yy = zip(*points)
    plt.scatter(xx, yy, **kwargs)


def draw_hull(points: list[tuple[float, float]], **kwargs):
    xx, yy = zip(*points)
    xx = [*xx, points[0][0]]
    yy = [*yy, points[0][1]]
    plt.plot(xx, yy, **kwargs)


def draw_line(p1: tuple[float, float], p2: tuple[float, float], **kwargs):
    xx = [p1[0], p2[0]]
    yy = [p1[1], p2[1]]
    plt.plot(xx, yy, **kwargs)


def circle_point(point: tuple[float, float], **kwargs):
    for k, v in {
        's': 80,
        'facecolors': 'none',
        'edgecolors': 'r'
    }.items():
        if k not in kwargs:
            kwargs[k] = v
    plt.scatter(point[0], point[1], **kwargs)


title = plt.title

show_plot = plt.show
