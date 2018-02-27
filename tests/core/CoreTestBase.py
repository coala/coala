import unittest

from coalib.core.Core import run


class CoreTestBase(unittest.TestCase):
    def execute_run(self, bears, cache=None, executor=None):
        """
        Executes a coala run and returns the results.

        This function has multiple ways to provide a different executor than
        the default one (topmost item has highest precedence):

        - Pass it via the ``executor`` parameter.
        - Assign an executor class and the according instantiation arguments to
          ``self.executor`` during ``setUp()``.

        :param bears:
            The bears to run.
        :param cache:
            A cache the bears can use to speed up runs. If ``None``, no cache
            will be used.
        :param executor:
            The executor to run bears on.
        :return:
            A list of results.
        """
        if executor is None:
            executor = getattr(self, 'executor', None)
            if executor is not None:
                cls, args, kwargs = self.executor
                executor = cls(*args, **kwargs)

        results = []

        def capture_results(result):
            results.append(result)

        run(bears, capture_results, cache, executor)

        return results
