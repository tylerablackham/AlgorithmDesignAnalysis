import argparse
import math
import random
from math import inf
from time import time

from plotting import plot_points, draw_path, circle_point, title, show_plot, plot_weights
from network_routing import find_shortest_path_with_array, find_shortest_path_with_heap


def rand1to1():
    return (random.random() - 0.5) * 2  # -1 to 1


def dist(p1, p2, noise):
    if noise == -1:
        return random.random()

    raw_dist = math.dist(p1, p2)

    return max(0.0, raw_dist + random.normalvariate(mu=0, sigma=noise))


def generate_graph(seed, size, density, noise) -> tuple[
    list[tuple[float, float]],   # The positions
    dict[int, dict[int, float]]  # The graph
]:
    random.seed(seed)

    positions = [
        (rand1to1(), rand1to1())
        for _ in range(size)
    ]

    edges_per_node = int(round((size - 1) * density))

    weights = {}
    for source in range(size):
        weights[source] = {}
        for target in random.sample(range(size), edges_per_node):
            weights[source][target] = dist(positions[source], positions[target], noise)

    return positions, weights


def main(seed: int, size: int, density: float, noise: float, source: int, target: int):
    start = time()
    positions, weights = generate_graph(seed, size, density, noise)
    end = time()

    num_edges = sum(len(edges) for edges in weights.values())
    print(f'Time to generate network of {size} nodes and {num_edges} edges: {round(end - start, 4)}')

    print(f'Direct cost from {source} to {target}: {weights[source].get(target, math.inf)}')

    plot_points(positions)
    if num_edges < 50:
        # If the number of non-inf edges is < 50
        plot_weights(positions, weights)

    circle_point(positions[source], c='r')
    circle_point(positions[target], c='b')

    start = time()
    path, cost = find_shortest_path_with_heap(weights, source, target)
    end = time()
    heap_time = end - start
    print()
    print('-- Heap --')
    print('Path:', path)
    print('Cost:', cost)
    print('Time:', heap_time)

    draw_path(positions, path)

    start = time()
    path, cost = find_shortest_path_with_array(weights, source, target)
    end = time()
    array_time = end - start
    print()
    print('-- Array --')
    print('Path:', path)
    print('Cost:', cost)
    print('Time:', array_time)

    title(f'Cost: {cost}, Heap: {round(heap_time, 4)}, Array: {round(array_time, 4)}')
    show_plot()


if __name__ == '__main__':
    # To debug or run in your IDE
    # you can uncomment the lines below and modify the arguments as needed
    import sys
    sys.argv = ['main.py', '-n', '6000']

    parser = argparse.ArgumentParser()
    parser.add_argument('-n', type=int, help='The number of points to generate', default=10)
    parser.add_argument('--seed', type=int, default=312, help='Random seed')
    parser.add_argument('--density', type=float, default=1, help='Fraction of non-inf edges')
    parser.add_argument('--noise', type=float, default=0.2, help='How non-euclidean are the edge weights')
    parser.add_argument('--source', type=int, default=2, help='Starting node')
    parser.add_argument('--target', type=int, default=9, help='Target node')
    parser.add_argument('--debug', action='store_true', help='Turn on debug plotting')
    args = parser.parse_args()

    if args.debug:
        # To debug your algorithm with incremental plotting:
        # - run this script with --debug (e.g. add '--debug' to the sys.argv above)
        # - set breakpoints
        # As you step through your code, you will see the plot update as you go
        import matplotlib.pyplot as plt

        plt.switch_backend('QtAgg')
        plt.ion()

    if args.target is None:
        args.target = args.n - 1

    main(args.seed, args.n, args.density, args.noise, args.source, args.target)

    # You can use a loop like the following to generate data for your tables:
    # for n in [100, 200, 400, 800, 1600, 3200, 6400]:
    #     main(312, n, 1, 0.05, 2, 9)
