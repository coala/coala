from itertools import tee


def pairwise(iterable):
    """
    Yields elements pairwise from the given iterable.

    Concretely: ``s -> (s0,s1), (s1,s2), (s2, s3), ...``

    :param iterable: The iterable to yield pairwise for.
    :return:         A new iterable yielding pairwise.
    """

    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)
