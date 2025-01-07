import math

import matplotlib.pyplot as plt

from tsp_core import (generate_network, Timer, Solver, SolutionStats)
from tsp_plot import (plot_solutions, plot_solution_progress_compared, plot_tour)


def format_text_summary(name: str, stats: SolutionStats):
    return (
        f'--------- {name} ---------\n'
        f'Score: {round(stats.score, 3)} \n'
        f'Time: {round(stats.time, 4)} sec \n'
        f'Coverage: {round(stats.fraction_leaves_covered * 100, 4)}% covered \n'
        f'Max Queue Size: {stats.max_queue_size} \n'
        f'# nodes expanded: {stats.n_nodes_expanded} \n'
        f'# nodes pruned: {stats.n_nodes_pruned}\n'
    )


def format_plot_summary(name: str, stats: SolutionStats):
    return (
        f'{name}: {round(stats.score, 3)} '
        f'({round(stats.time, 4)} sec, '
        f'{round(stats.fraction_leaves_covered * 100, 4)}% covered)'
    )


def main(n, *find_tours: Solver, timeout=60, **kwargs):
    # Generate
    print(f'Generating network of size {n} with args: {kwargs}')
    locations, edges = generate_network(n, **kwargs)

    # Solve
    print('Running TSP Solvers...')

    all_stats = {}
    find_tour: Solver
    for find_tour in find_tours:
        timer = Timer(timeout)
        stats = find_tour(edges, timer)
        name = find_tour.__name__
        all_stats[name] = stats
        if stats:
            print(format_text_summary(name, stats[-1]))
        else:
            print(f'No solutions for {name}')
            print()

    # Report and Plot
    n_plots = 2  # solutions, solution progress
    n_plots += len(all_stats)  # tours

    fig, axs = plt.subplots(n_plots, 1, figsize=(8, 8 * n_plots))
    axs = axs.flatten()

    plot_solutions(all_stats, axs[0])

    plot_solution_progress_compared(
        {
            name: all_stats[name][-1].tour
            for name in all_stats
            if not math.isinf(all_stats[name][-1].score)
        }, edges, ax=axs[1])

    for (name, stats), ax in zip(all_stats.items(), axs[2:]):
        plot_tour(locations, stats[-1].tour, ax=ax)
        ax.set_title(f'{name} ({stats[-1].score})')

    plt.show()


if __name__ == '__main__':
    from tsp_solve import (random_tour, greedy_tour, dfs, branch_and_bound, branch_and_bound_smart)

    main(
        150,
        random_tour,
        greedy_tour,
        dfs,
        branch_and_bound,
        branch_and_bound_smart,
        euclidean=True,
        reduction=0.2,
        normal=False,
        seed=122,
        timeout=60
    )
