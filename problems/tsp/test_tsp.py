import math

from byu_pytest_utils import max_score
from tsp_core import Timer, generate_network, score_tour
from math import inf

from tsp_solve import greedy_tour, dfs, branch_and_bound, branch_and_bound_smart

""" 
---- IMPORTANT ----

If your implementation of any of these algorithms
uses too much RAM, your tests will crash in gradescope
and you will get no credit for any of them.

Run these tests locally and monitor your RAM usage. 
"""


def assert_valid_tour(edges, tour):
    """
    Length is number of vertices
    Not vertices repeated
    Non-infinite score
    """
    assert len(tour) == len(edges)
    assert len(tour) == len(set(tour))
    assert not math.isinf(score_tour(tour, edges))


def assert_valid_tours(edges, stats):
    for stat in stats:
        assert_valid_tour(edges, stat.tour)


@max_score(5)
def test_greedy():
    graph = [
        [0, 9, inf, 8, inf],
        [inf, 0, 4, inf, 2],
        [inf, 3, 0, 4, inf],
        [inf, 6, 7, 0, 12],
        [1, inf, inf, 10, 0]
    ]
    timer = Timer(10)
    stats = greedy_tour(graph, timer)
    assert_valid_tours(graph, stats)

    assert stats[0].tour == [1, 4, 0, 3, 2]
    assert stats[0].score == 21

    assert len(stats) == 1


@max_score(5)
def test_dfs():
    graph = [
        [0, 9, inf, 8, inf],
        [inf, 0, 4, inf, 2],
        [inf, 3, 0, 4, inf],
        [inf, 6, 7, 0, 12],
        [1, inf, inf, 10, 0]
    ]
    timer = Timer(10)
    stats = dfs(graph, timer)
    assert_valid_tours(graph, stats)

    scores = {
        tuple(stat.tour): stat.score
        for stat in stats
    }
    assert scores[0, 3, 2, 1, 4] == 21
    assert len(scores) == 1


@max_score(10)
def test_branch_and_bound():
    """
    - Greedy should run almost instantly.
    - B&B should search the entire space in less than 3 minutes.
      (A good implementation should finish in seconds).
    - B&B should find a better score than greedy (on this graph).
    """

    locations, edges = generate_network(
        15,
        euclidean=True,
        reduction=0.2,
        normal=False,
        seed=312,
    )

    timer = Timer(5)
    greedy_stats = greedy_tour(edges, timer)
    assert not timer.time_out()
    assert_valid_tours(edges, greedy_stats)

    timer = Timer(120)
    stats = branch_and_bound_smart(edges, timer)
    assert not timer.time_out()
    assert_valid_tours(edges, stats)

    assert stats[-1].score < greedy_stats[-1].score


@max_score(10)
def test_branch_and_bound_smart():
    """
    Your Smart B&B algorithm should find a better answer
    than your B&B algorithm in the same amount of time.
    """

    locations, edges = generate_network(
        30,
        euclidean=True,
        reduction=0.2,
        normal=False,
        seed=312,
    )

    timer = Timer(20)
    bnb_stats = branch_and_bound(edges, timer)
    assert_valid_tours(edges, bnb_stats)

    timer = Timer(20)
    stats = branch_and_bound_smart(edges, timer)
    assert_valid_tours(edges, stats)

    assert stats[-1].score < bnb_stats[-1].score


@max_score(5)
def test_extra_credit_branch_and_bound_smart():
    locations, edges = generate_network(
        50,
        euclidean=True,
        reduction=0.2,
        normal=False,
        seed=4321,
    )

    timer = Timer(10)
    stats = branch_and_bound_smart(edges, timer)
    assert_valid_tours(edges, stats)

    # On this same graph, Professor Bean's B&B algorithm
    # got a score of 7.610 in 10 seconds
    # and his modified B&B algorithm
    # got a score of 7.038 in 10 seconds
    # If you beat this score, you get extra credit
    assert stats[-1].score < 7.039
