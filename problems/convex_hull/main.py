import argparse
from time import time

from generate import generate_random_points
from convex_hull import compute_hull
from plotting import plot_points, draw_hull, title, show_plot


def main(n: int, distribution: str, seed: int | None):
    points = generate_random_points(distribution, n, seed)
    plot_points(points)

    start = time()
    hull_points = compute_hull(points)
    end = time()

    draw_hull(hull_points)
    print(f'{n} {distribution} points: {round(end - start, 4)} seconds')
    show_plot()


if __name__ == '__main__':

    # To debug or run in your IDE
    # you can uncomment the lines below and modify the arguments as needed
    # import sys
    # sys.argv = ['main.py', '-n', '10', '--seed', '312', '--debug']

    parser = argparse.ArgumentParser()
    parser.add_argument('-n', type=int, help='The number of points to generate', default=10)
    parser.add_argument('-d', '--dist', '--distribution',
                        help='The distribution from which to generate points',
                        default='uniform'
                        )
    parser.add_argument('--seed', type=int, default=None, help="Random seed")
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
    for i in [10,100,1000,10000, 100000, 500000, 1000000]:
        for j in range(5):
            main(i, args.dist, args.seed)
