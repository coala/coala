from collections import Iterable
from functools import partial
import unittest

from coalib.core.CircularDependencyError import CircularDependencyError
from coalib.core.Graphs import traverse_graph


def get_successive_nodes(graph, node):
    try:
        item = graph[node]
    except KeyError:
        return set()

    if isinstance(item, Iterable):
        return item
    else:
        return {item}


def traverse_graph_on_cyclic_graph_test(graph, start_nodes):
    """
    Tests whether ``traverse_graph`` throws a ``CircularDependencyError`` on
    a given cyclic graph.

    :param graph:
        The cyclic graph to test.
    :param start_nodes:
        The nodes where to start walking from.
    """

    def test_function(self):
        with self.assertRaises(CircularDependencyError) as cm:
            traverse_graph(start_nodes, partial(get_successive_nodes, graph))

    return test_function


def traverse_graph_test(graph, start_nodes, expected):
    """
    Creates a test which tests the ``traverse_graph`` function.

    :param graph:
        The graph organized as a dict which contains all edges of the graph.
    :param start_nodes:
        The start nodes where to start walking the graph from.
    :param expected:
        The iterable of expected edges. Each edge is denoted as a tuple pair.
    :return:
        A test function testing ``test_traverse_graph``.
    """

    def test_function(self):
        results = []

        def append_to_results(prev, nxt):
            results.append((prev, nxt))

        traverse_graph(start_nodes,
                       partial(get_successive_nodes, graph),
                       append_to_results)

        # Test if edges were walked twice.
        result_set = set(results)

        remaining_results = list(results)
        for elem in result_set:
            remaining_results.remove(elem)

        self.assertEqual(len(remaining_results), 0,
                         'Edge(s) walked twice: ' + ', '.join(
                             str(r) for r in remaining_results))

        # Compare real with expected without respecting order.
        expected_set = set(expected)
        self.assertEqual(result_set, expected_set)

    return test_function


class GraphsTest(unittest.TestCase):
    test_traverse_graph_multi_entrypoints_single_path = traverse_graph_test(
        {1: 2, 2: 3, 3: 4},
        {1, 2},
        {(1, 2), (2, 3), (3, 4)})

    test_traverse_graph_late_entrypoint = traverse_graph_test(
        {1: 2, 2: 3, 3: 4},
        {3},
        {(3, 4)})

    test_traverse_graph_big_graph = traverse_graph_test(
        {1: 2, 3: 4, 4: 5, 5: [6, 7], 6: [8, 9, 10], 9: 10, 7: 11},
        {1, 3},
        {(1, 2), (3, 4), (4, 5), (5, 6), (6, 8), (6, 9), (6, 10), (9, 10),
         (5, 7), (7, 11)})

    test_traverse_graph_big_graph_multi_entrypoint = traverse_graph_test(
        {1: 2, 3: 4, 4: 5, 5: [6, 7], 6: [8, 9, 10], 9: 10, 7: 11},
        {1, 3, 6, 9, 4},
        {(1, 2), (3, 4), (4, 5), (5, 6), (6, 8), (6, 9), (6, 10), (9, 10),
         (5, 7), (7, 11)})

    test_traverse_graph_big_graph_primitive_entrypoint = traverse_graph_test(
        {1: 2, 3: 4, 4: 5, 5: [6, 7], 6: [8, 9, 10], 9: 10, 7: [5, 11], 10: 7},
        {1},
        {(1, 2)})

    test_traverse_graph_complex_graph = traverse_graph_test(
        {1: 2, 2: [4, 8], 3: [2, 4], 4: [5, 12], 5: [6, 7], 6: [7, 8, 9, 10],
         7: 11, 9: 10, 10: [7, 11], 12: 6},
        {1, 3, 9, 7},
        {(1, 2), (2, 4), (2, 8), (3, 2), (3, 4), (4, 5), (4, 12), (5, 6),
         (5, 7), (6, 7), (6, 8), (6, 9), (6, 10), (7, 11), (9, 10), (10, 7),
         (10, 11), (12, 6)})

    test_traverse_graph_empty_graph_multi_entrypoints = traverse_graph_test(
        {},
        {1, 2, 3},
        set())

    test_traverse_graph_empty_graph_no_entrypoints = traverse_graph_test(
        {},
        set(),
        set())

    test_traverse_graph_no_entrypoints = traverse_graph_test(
        {1: 2, 2: 3},
        set(),
        set())

    test_traverse_graph_cyclic_simple1 = traverse_graph_on_cyclic_graph_test(
        {1: 2, 2: 3, 3: 1},
        {1})

    test_traverse_graph_cyclic_simple2 = traverse_graph_on_cyclic_graph_test(
        {1: 2, 2: 3, 3: 1},
        {2})

    test_traverse_graph_cyclic_complex1 = traverse_graph_on_cyclic_graph_test(
        {1: 2, 3: 4, 4: 5, 5: [6, 7], 6: [8, 9, 10], 9: 10, 7: [5, 11], 10: 7},
        {3})

    test_traverse_graph_cyclic_complex2 = traverse_graph_on_cyclic_graph_test(
        {1: 2, 2: [4, 8], 3: [2, 4], 4: [5, 12], 5: [6, 7], 6: [7, 8, 9, 10],
         7: 11, 9: 10, 10: [3, 7, 11], 12: 6},
        {1, 3})
