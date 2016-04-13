from contextlib import contextmanager
import os
import pkg_resources
import sys

from coalib.misc.ContextManagers import retrieve_stdout


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
        retval = func()
        return retval, stdout.getvalue()


@contextmanager
def bear_test_module():
    """
    This function replaces the pkg_resources.iter_entry_points()
    to use the testing bear module we have. Hence, it doesn't test
    the collection of entry points.
    """
    old_iter = pkg_resources.iter_entry_points
    bears_test_module = os.path.join(os.path.dirname(__file__),
                                     "test_bears",
                                     "__init__.py")

    def test_iter_entry_points(name):
        assert name == "coalabears"

        class EntryPoint:

            @staticmethod
            def load():
                class PseudoPlugin:
                    __file__ = bears_test_module
                return PseudoPlugin()

        return iter([EntryPoint()])

    pkg_resources.iter_entry_points = test_iter_entry_points
    try:
        yield
    finally:
        pkg_resources.iter_entry_points = old_iter
