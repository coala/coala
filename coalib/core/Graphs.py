from coalib.core.CircularDependencyError import CircularDependencyError


def traverse_graph(start_nodes, get_successive_nodes,
                   run_on_edge=lambda prev, nxt: None):
    """
    Traverses all edges of a directed, possibly disconnected graph once.
    Detects cyclic graphs by raising a ``CircularDependencyError``.

    >>> graph = {1: [2], 2: [3, 4], 5: [3], 3: [6]}
    >>> def get_successive_nodes(node):
    ...     return graph.get(node, [])
    >>> edges = set()
    >>> def append_to_edges(prev, nxt):
    ...     edges.add((prev, nxt))
    >>> traverse_graph([1, 5], get_successive_nodes, append_to_edges)
    >>> sorted(edges)
    [(1, 2), (2, 3), (2, 4), (3, 6), (5, 3)]

    You can also use this function to detect cyclic graphs:

    >>> graph = {1: [2], 2: [3], 3: [1]}
    >>> traverse_graph([1], get_successive_nodes)
    Traceback (most recent call last):
     ...
    coalib.core.CircularDependencyError.CircularDependencyError: ...

    :param start_nodes:
        The nodes where to start traversing the graph.
    :param get_successive_nodes:
        A callable that takes in a node and returns an iterable of nodes to
        traverse next.
    :param run_on_edge:
        A callable that is run on each edge during traversing. Takes in two
        parameters, the previous- and next-node which form an edge. The default
        is an empty function.
    :raises CircularDependencyError:
        Raised when the graph is cyclic.
    """
    path = set()
    visited_nodes = set()

    def visit(node):
        if node not in visited_nodes:
            visited_nodes.add(node)
            path.add(node)

            for subnode in get_successive_nodes(node):
                run_on_edge(node, subnode)

                if subnode in path:
                    raise CircularDependencyError([repr(subnode), '...',
                                                   repr(subnode)])
                visit(subnode)

            path.remove(node)

    for node in start_nodes:
        visit(node)
