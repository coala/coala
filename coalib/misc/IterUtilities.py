from itertools import tee


def partition(iterable, predicate):
    """
    Partitions the iterable into two iterables based on the given predicate.

    :param predicate:   A function that takes an item of the iterable and
                        returns a boolean
    :return:            Two iterators pointing to the original iterable
    """
    a, b = tee((predicate(item), item) for item in iterable)

    return ((item for pred, item in a if pred),
            (item for pred, item in b if not pred))
