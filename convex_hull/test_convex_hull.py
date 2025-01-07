from byu_pytest_utils import max_score

from test_utils import is_convex_hull

from convex_hull import compute_hull
from generate import generate_random_points


@max_score(5)
def test_uniform_distribution_small():
    points = generate_random_points('uniform', 10, 312)
    candidate_hull = compute_hull(points)
    assert is_convex_hull(candidate_hull, points)


@max_score(15)
def test_uniform_distribution_large():
    points = generate_random_points('uniform', 20000, 312)
    candidate_hull = compute_hull(points)
    assert is_convex_hull(candidate_hull, points)


@max_score(5)
def test_guassian_distribution_small():
    points = generate_random_points('guassian', 10, 312)
    candidate_hull = compute_hull(points)
    assert is_convex_hull(candidate_hull, points)


@max_score(15)
def test_guassian_distribution_large():
    points = generate_random_points('guassian', 20000, 312)
    candidate_hull = compute_hull(points)
    assert is_convex_hull(candidate_hull, points)
