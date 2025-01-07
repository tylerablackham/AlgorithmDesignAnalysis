import dataclasses
import random
import math
import time

from typing import NamedTuple, Protocol


class Timer:
    def __init__(self, time_limit: float = 60):
        self.start = time.time()
        self.time_limit = time_limit

    def time(self) -> float:
        return time.time() - self.start

    def time_out(self) -> bool:
        return self.time() > self.time_limit


# List of cities in the tour
# Assumes the last city returns to the first
Tour = list[int]


@dataclasses.dataclass
class SolutionStats:
    tour: list[int]
    score: float
    time: float
    max_queue_size: int
    n_nodes_expanded: int
    n_nodes_pruned: int
    n_leaves_covered: int
    fraction_leaves_covered: float


class Solver(Protocol):
    """
    Method signature for a function that takes a matrix of edge weights and returns a tour
    """

    def __call__(self,
                 edges: list[list[float]],
                 timer: Timer
                 ) -> list[SolutionStats]: ...


class Location(NamedTuple):
    x: float
    y: float


def _euclidean_dist(loc1: Location, loc2: Location) -> float:
    a1, b1 = loc1
    a2, b2 = loc2
    return math.sqrt((a1 - a2) ** 2 + (b1 - b2) ** 2)


def generate_network(
        n: int,
        seed: int | None = None,
        reduction: float = 0.0,
        euclidean: bool = True,
        normal: bool = False,
) -> tuple[list[Location], list[list[float]]]:
    """
    Generate a random network of cities.

    :param n: How many cities
    :param seed: Seed for random.seed(). Use None for default (system time).
    :param reduction: Fraction of edges to remove
    :param euclidean: Whether to use Euclidean weights
    :param normal: Whether to use normally-distributed weights (requires euclidean=True)
    :return: The locations of the cities and an n x n matrix of edge weights
    """

    random.seed(seed)

    locations = [
        Location(random.random(), random.random())
        for _ in range(n)
    ]

    random_weight = (lambda: random.gauss(mu=0.0, sigma=1.0)) if normal else random.random
    _dist = _euclidean_dist if euclidean else lambda a, b: random_weight()

    edges = [
        [
            math.inf
            if (random.random() < reduction)
            else round(_dist(locations[s], locations[t]), 3)
            for t in range(n)
        ]
        for s in range(n)
    ]

    return locations, edges


def get_segments(tour: Tour) -> list[tuple[int, int]]:
    return list(zip(tour[:-1], tour[1:])) + [(tour[-1], tour[0])]


def score_tour(tour: Tour, edges: list[list[float]]) -> float:
    score = 0
    for s, t in get_segments(tour):
        score += edges[s][t]
    return score


def score_partial_tour(partial_tour: Tour, edges: list[list[float]]) -> float:
    score = 0
    for s, t in get_segments(partial_tour)[:-1]:  # exclude the back-to-initial leg
        score += edges[s][t]
    return score
