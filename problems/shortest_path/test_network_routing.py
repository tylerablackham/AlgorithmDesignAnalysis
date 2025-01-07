from byu_pytest_utils import max_score, with_import

from main import generate_graph


def tiny_test(finder):
    graph = {
        0: {1: 2, 2: 1, 3: 4},
        1: {0: 2, 2: 1, 3: 1},
        2: {0: 4, 1: 4},
        3: {0: 3, 1: 2, 2: 1}
    }
    path, cost = finder(
        graph, 0, 3
    )

    assert path == [0, 1, 3]
    assert cost == 3


def small_test(finder):
    _, graph = generate_graph(312, 10, 0.3, 0.05)
    path, cost = finder(graph, 0, 9)
    assert path == [0, 4, 9]
    assert round(cost, 2) == 2.08


def large_test(finder):
    _, graph = generate_graph(312, 1000, 0.2, 0.05)
    path, cost = finder(graph, 2, 9)
    assert path == [2, 391, 90, 956, 227, 236, 133, 429, 697, 846, 148, 775, 359, 685, 335, 102, 315, 9]
    assert round(cost, 2) == 1.12


@max_score(2)
@with_import('network_routing')
def test_tiny_network_heap(find_shortest_path_with_heap):
    tiny_test(find_shortest_path_with_heap)


@max_score(2)
@with_import('network_routing')
def test_tiny_network_array(find_shortest_path_with_array):
    tiny_test(find_shortest_path_with_array)


@max_score(5)
@with_import('network_routing')
def test_small_network_heap(find_shortest_path_with_heap):
    small_test(find_shortest_path_with_heap)


@max_score(5)
@with_import('network_routing')
def test_small_network_array(find_shortest_path_with_array):
    small_test(find_shortest_path_with_array)


@max_score(8)
@with_import('network_routing')
def test_large_network_heap(find_shortest_path_with_heap):
    large_test(find_shortest_path_with_heap)


@max_score(8)
@with_import('network_routing')
def test_large_network_array(find_shortest_path_with_array):
    large_test(find_shortest_path_with_array)
