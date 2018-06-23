import functools


class memoized_property:
    """
    ``memoized_property`` serves as a decorator to cache
    the results of the properties like ``raw``, ``string``
    and ``lines`` provided by ``FileFactory``.
    """

    def __init__(self, method):
        self._method = method
        functools.update_wrapper(self, method)

    def __get__(self, instance, owner):
        try:
            result = instance.cache[self._method]
        except KeyError:
            result = self._method(instance)
            instance.cache[self._method] = result
        return result
