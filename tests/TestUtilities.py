from contextlib import contextmanager
import os
import sys
import unittest.mock

from coalib.misc.ContextManagers import retrieve_stdout, retrieve_stderr


def execute_coala(func, binary, *args):
    """
    Executes the main function with the given argument string from given module.

    :param function: A main function from coala_json, coala_ci module etc.
    :param binary:   A binary to execute coala test
    :return:         A tuple holding a return value first and
                     a stdout output as second element.
    """
    sys.argv = [binary] + list(args)
    with retrieve_stdout() as stdout:
        with retrieve_stderr() as stderr:
            retval = func()
            return retval, stdout.getvalue() + '\n' + stderr.getvalue()


@contextmanager
def bear_test_module():
    """
    This function mocks the ``pkg_resources.iter_entry_points()``
    to use the testing bear module we have. Hence, it doesn't test
    the collection of entry points.
    """
    bears_test_module = os.path.join(os.path.dirname(__file__),
                                     "test_bears", "__init__.py")

    class EntryPoint:

        @staticmethod
        def load():
            class PseudoPlugin:
                __file__ = bears_test_module
            return PseudoPlugin()

    with unittest.mock.patch("pkg_resources.iter_entry_points",
                             return_value=[EntryPoint()]) as mocked:
        yield
