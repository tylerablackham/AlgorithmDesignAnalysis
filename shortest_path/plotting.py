import math

import matplotlib.pyplot as plt


def plot_points(positions: list[tuple[float, float]], **kwargs):
    if 'c' not in kwargs:
        kwargs['c'] = 'k'

    xx, yy = zip(*positions)
    plt.scatter(xx, yy, **kwargs)


def plot_weights(
        positions: list[tuple[float, float]],
        weights: dict[int, dict[int, float]],
        **kwargs
):
    kwargs['c'] = kwargs.get('c', 'k')

    max_w = max(max(edges.values()) for edges in weights.values())

    for source, edges in weights.items():
        for target, w in edges.items():
            xx = [positions[source][0], positions[target][0]]
            yy = [positions[source][1], positions[target][1]]
            alpha = w / max_w
            plt.plot(xx, yy, alpha=alpha, **kwargs)


def draw_path(positions: list[tuple[float, float]], path: list[int], **kwargs):
    path_positions = [positions[p] for p in path]
    xx, yy = zip(*path_positions)

    kwargs['alpha'] = kwargs.get('alpha', 0.5)
    kwargs['lw'] = kwargs.get('lw', 5)

    plt.plot(xx, yy, **kwargs)


def circle_point(point: tuple[float, float], **kwargs):
    for k, v in {
        's': 100
    }.items():
        if k not in kwargs:
            kwargs[k] = v
    plt.scatter(point[0], point[1], **kwargs)


title = plt.title

show_plot = plt.show
