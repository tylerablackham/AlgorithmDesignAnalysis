import math
from math import inf
import random
import heapq

from tsp_core import Tour, SolutionStats, Timer, score_tour, Solver
from tsp_cuttree import CutTree


def is_solution(tour: list[float], edges: list[list[float]]):
    if len(tour) != len(edges):
        return False
    if math.isinf(edges[tour[-1]][tour[0]]):
        return False
    return True


def random_tour(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    stats = []
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    cut_tree = CutTree(len(edges))

    while True:
        if timer.time_out():
            return stats

        tour = random.sample(list(range(len(edges))), len(edges))
        n_nodes_expanded += 1

        cost = score_tour(tour, edges)
        if math.isinf(cost):
            n_nodes_pruned += 1
            cut_tree.cut(tour)
            continue

        if stats and cost > stats[-1].score:
            n_nodes_pruned += 1
            cut_tree.cut(tour)
            continue

        stats.append(SolutionStats(
            tour=tour,
            score=cost,
            time=timer.time(),
            max_queue_size=1,
            n_nodes_expanded=n_nodes_expanded,
            n_nodes_pruned=n_nodes_pruned,
            n_leaves_covered=cut_tree.n_leaves_cut(),
            fraction_leaves_covered=cut_tree.fraction_leaves_covered()
        ))

    if not stats:
        return [SolutionStats(
            [],
            math.inf,
            timer.time(),
            1,
            n_nodes_expanded,
            n_nodes_pruned,
            cut_tree.n_leaves_cut(),
            cut_tree.fraction_leaves_covered()
        )]


def greedy_tour(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    nodes_expanded = 0
    nodes_pruned = 0
    cut_tree = CutTree(len(edges))
    for start in range(len(edges)):
        nodes_expanded += 1
        temp_tour = [start]
        temp_score = 0
        current = start
        solution_found = False
        rows_left = list(range(len(edges)))
        while True:
            min_edge = inf
            best_dest = None
            rows_left.remove(current)
            for dest in rows_left:
                if edges[current][dest] < min_edge:
                    min_edge = edges[current][dest]
                    best_dest = dest
            if best_dest is None:
                cut_tree.cut(temp_tour)
                nodes_pruned += 1
                break
            temp_tour.append(best_dest)
            temp_score += min_edge
            current = best_dest
            if is_solution(temp_tour, edges):
                solution_found = True
                temp_score += edges[current][start]
                break
        if solution_found:
            return [
                SolutionStats(
                    tour=temp_tour,
                    score=temp_score,
                    time=timer.time(),
                    max_queue_size=1,
                    n_nodes_expanded=nodes_expanded,
                    n_nodes_pruned=nodes_pruned,
                    n_leaves_covered=cut_tree.n_leaves_cut(),
                    fraction_leaves_covered=cut_tree.fraction_leaves_covered()
                )
            ]
    return [SolutionStats(
        tour=[],
        score=math.inf,
        time=timer.time(),
        max_queue_size=1,
        n_nodes_expanded=nodes_expanded,
        n_nodes_pruned=nodes_pruned,
        n_leaves_covered=cut_tree.n_leaves_cut(),
        fraction_leaves_covered=cut_tree.fraction_leaves_covered()
    )]


def dfs(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    solution_stats = []
    max_queue_size = 1
    nodes_expanded = 0
    cut_tree = CutTree(len(edges))
    best_score = math.inf
    stack = [([0], 0)]
    while len(stack) > 0:
        if timer.time_out():
            break
        tour, score = stack.pop(0)
        nodes_expanded += 1
        current = tour[-1]
        for dest in range(len(edges)):
            if dest in tour:
                pass
            else:
                new_tour = tour + [dest]
                new_score = score + edges[current][dest]
                if is_solution(new_tour, edges) and new_score < best_score:
                    best_score = new_score + edges[dest][0]
                    solution_stats.append(SolutionStats(
                        tour=new_tour,
                        score=best_score,
                        time=timer.time(),
                        max_queue_size=max_queue_size,
                        n_nodes_expanded=nodes_expanded,
                        n_nodes_pruned=0,
                        n_leaves_covered=cut_tree.n_leaves_cut(),
                        fraction_leaves_covered=cut_tree.fraction_leaves_covered()
                    ))
                else:
                    stack.insert(0, (new_tour, new_score))
                    max_queue_size = max(max_queue_size, len(stack))
    if len(solution_stats) == 0:
        solution_stats.append(SolutionStats(
            tour=[],
            score=math.inf,
            time=timer.time(),
            max_queue_size=max_queue_size,
            n_nodes_expanded=nodes_expanded,
            n_nodes_pruned=0,
            n_leaves_covered=cut_tree.n_leaves_cut(),
            fraction_leaves_covered=cut_tree.fraction_leaves_covered()
        ))
    return solution_stats


def create_rcm(rcm: dict[tuple[int, int], float], initial_lb: float,
               rows_left: list[int], cols_left: list[int]) -> tuple[dict[tuple[int, int], float], float]:
    for row in rows_left:
        min_row_edge = math.inf
        for col in cols_left:
            min_row_edge = min(min_row_edge, rcm[(row, col)])
        for col in cols_left:
            rcm[(row, col)] = rcm[(row, col)] - min_row_edge
        initial_lb += min_row_edge
    for col in cols_left:
        min_col_edge = math.inf
        for row in rows_left:
            min_col_edge = min(min_col_edge, rcm[(row, col)])
        for row in rows_left:
            rcm[(row, col)] = rcm[(row, col)] - min_col_edge
        initial_lb += min_col_edge
    return rcm, initial_lb


def update_rcm(initial_rcm: dict[tuple[int, int], float], initial_lb: float,
               rows_left: list[int], cols_left: list[int], current: int, dest: int) -> tuple[dict[tuple[int, int], float], float]:
    initial_lb += initial_rcm[(current, dest)]
    if initial_lb == math.inf:
        return initial_rcm, initial_lb
    else:
        rcm = initial_rcm.copy()
        for row in rows_left:
            rcm.pop((row, dest))
        for col in cols_left:
            rcm.pop((current, col))
        rcm.pop((current, dest))
        rcm[(dest, current)] = math.inf
        return create_rcm(rcm, initial_lb, rows_left, cols_left)


def branch_and_bound_smart(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    n = len(edges)
    solution_stats = []
    cut_tree = CutTree(n)
    nodes_pruned, nodes_expanded, max_queue_size = 0, 0, 1
    bssf = greedy_tour(edges, timer)[0].score
    rows_left = list(range(n))
    cols_left = list(range(n))
    initial_rcm = dict()
    for row in rows_left:
        for col in cols_left:
            initial_rcm[(row, col)] = edges[row][col]
    initial_rcm, initial_lb = create_rcm(initial_rcm, 0, rows_left, cols_left)
    stack = [(initial_rcm, initial_lb, rows_left, cols_left, [0])]
    while len(stack) > 0:
        if timer.time_out():
            break
        rcm, lb, rows_left, cols_left, tour = stack.pop()
        if lb > bssf:
            nodes_pruned += 1
            cut_tree.cut(tour)
        else:
            nodes_expanded += 1
            current = tour[-1]
            for dest in [x for x in cols_left if x != 0]:
                new_rows_left = [x for x in rows_left if x != current]
                new_cols_left = [x for x in cols_left if x != dest]
                new_rcm, new_lb = update_rcm(initial_rcm, initial_lb,
                                             new_rows_left, new_cols_left, current, dest)
                if new_lb > bssf:
                    nodes_pruned += 1
                    cut_tree.cut(tour)
                else:
                    new_tour = tour + [dest]
                    if is_solution(new_tour, edges):
                        bssf = new_lb
                        solution_stats.append(SolutionStats(
                            tour=new_tour,
                            score=new_lb,
                            time=timer.time(),
                            max_queue_size=max_queue_size,
                            n_nodes_expanded=nodes_expanded,
                            n_nodes_pruned=nodes_pruned,
                            n_leaves_covered=cut_tree.n_leaves_cut(),
                            fraction_leaves_covered=cut_tree.fraction_leaves_covered()
                        ))
                    else:
                        stack.append((new_rcm, new_lb, new_rows_left, new_cols_left, new_tour))
                        max_queue_size = max(max_queue_size, len(stack))
    if len(solution_stats) == 0:
        solution_stats.append(SolutionStats(
            tour=[],
            score=math.inf,
            time=timer.time(),
            max_queue_size=max_queue_size,
            n_nodes_expanded=nodes_expanded,
            n_nodes_pruned=nodes_pruned,
            n_leaves_covered=cut_tree.n_leaves_cut(),
            fraction_leaves_covered=cut_tree.fraction_leaves_covered()
        ))
    return solution_stats

def branch_and_bound(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    n = len(edges)
    solution_stats = []
    cut_tree = CutTree(n)
    nodes_pruned, nodes_expanded, max_queue_size = 0, 0, 1
    bssf = greedy_tour(edges, timer)[0].score
    rows_left = list(range(n))
    cols_left = list(range(n))
    initial_rcm = dict()
    for row in rows_left:
        for col in cols_left:
            initial_rcm[(row, col)] = edges[row][col]
    initial_rcm, initial_lb = create_rcm(initial_rcm, 0, rows_left, cols_left)
    stack = [(0, initial_rcm, initial_lb, rows_left, cols_left, [0])]
    while len(stack) > 0:
        if timer.time_out():
            break
        _, rcm, lb, rows_left, cols_left, tour = stack.pop()
        if lb > bssf:
            nodes_pruned += 1
            cut_tree.cut(tour)
        else:
            nodes_expanded += 1
            current = tour[-1]
            children = []
            for dest in [x for x in cols_left if x != 0]:
                new_rows_left = [x for x in rows_left if x != current]
                new_cols_left = [x for x in cols_left if x != dest]
                new_rcm, new_lb = update_rcm(initial_rcm, initial_lb,
                                             new_rows_left, new_cols_left, current, dest)
                if new_lb > bssf:
                    nodes_pruned += 1
                    cut_tree.cut(tour)
                else:
                    new_tour = tour + [dest]
                    if is_solution(new_tour, edges):
                        bssf = new_lb
                        solution_stats.append(SolutionStats(
                            tour=new_tour,
                            score=new_lb,
                            time=timer.time(),
                            max_queue_size=max_queue_size,
                            n_nodes_expanded=nodes_expanded,
                            n_nodes_pruned=nodes_pruned,
                            n_leaves_covered=cut_tree.n_leaves_cut(),
                            fraction_leaves_covered=cut_tree.fraction_leaves_covered()
                        ))
                    else:
                        heapq.heappush(children, ((random.random()/100) - new_lb,
                                                  new_rcm, new_lb, new_rows_left, new_cols_left, new_tour))
            while len(children) > 0:
                stack.append(heapq.heappop(children))
            max_queue_size = max(max_queue_size, len(stack))
    if len(solution_stats) == 0:
        solution_stats.append(SolutionStats(
            tour=[],
            score=math.inf,
            time=timer.time(),
            max_queue_size=max_queue_size,
            n_nodes_expanded=nodes_expanded,
            n_nodes_pruned=nodes_pruned,
            n_leaves_covered=cut_tree.n_leaves_cut(),
            fraction_leaves_covered=cut_tree.fraction_leaves_covered()
        ))
    return solution_stats
