from contextlib import contextmanager
import os
import sys
import unittest.mock

from coala_utils.ContextManagers import retrieve_stdout, retrieve_stderr

# This list is sorted alphabetically
TEST_BEAR_NAMES = (
    'AspectsGeneralTestBear',
    'AspectTestBear',
    'DependentBear',
    'EchoBear',
    'ErrorTestBear',
    'JavaTestBear',
    'LineCountTestBear',
    'RaiseTestBear',
    'RaiseTestExecuteBear',
    'SpaceConsistencyTestBear',
    'TestBear',
    'TestDepBearA',
    'TestDepBearAA',
    'TestDepBearBDependsA',
    'TestDepBearCDependsB',
    'TestDepBearDependsAAndAA',
)

TEST_BEARS_COUNT = len(TEST_BEAR_NAMES)

JAVA_BEARS_COUNT = 3

C_BEARS_COUNT = 2

# This list is sorted alphabetically
LANGUAGE_NAMES = [
    'antlr 3, 4',
    'Bash',
    'C',
    'C#',
    'CPP',
    'CSS',
    'Extensible Markup Language 1.0',
    'Fortran',
    'Golang',
    'GraphQL',
    'Haskell 1.0, 1.1, 1.2, 1.3, 1.4, 98, 2010',
    'Hypertext Markup Language 2.0, 3.2, 4.0, 4.1, 5, 5.1',
    'Java',
    'JavaScript',
    'JavaScript Object Notation',
    'JavaServer Pages',
    'Jinja2',
    'KornShell',
    'Markdown',
    'Matlab',
    'ObjectiveC',
    'PHP',
    'PLSQL',
    'PowerShell',
    'Python 2.7, 3.3, 3.4, 3.5, 3.6',
    'Ruby',
    'Scala',
    'SCSS 3.1, 3.2, 3.3, 3.4, 3.5, 4.0',
    'Shell',
    'Swift',
    'Tcl',
    'TypeScript',
    'Vala',
    'VisualBasic',
    'm4',
    'ZShell',
]

LANGUAGE_COUNT = len([
     language_file[: -3] for language_file in
     os.listdir('coalib/bearlib/languages/definitions/')
     if language_file.endswith('.py') and language_file != '__init__.py'
     and language_file != 'Unknown.py'])

# This list is sorted by filename of the bears, then name within the modules
TEST_BEAR_NAME_REPRS = [
    "<class 'AspectTestBear.AspectTestBear'>",
    "<class 'AspectsGeneralTestBear.AspectsGeneralTestBear'>",
    "<ErrorTestBear linter class (wrapping 'I_do_not_exist')>",
    "<class 'JavaTestBear.JavaTestBear'>",
    "<class 'LineCountTestBear.LineCountTestBear'>",
    "<EchoBear linter class (wrapping 'echo')>",
    "<class 'RaiseTestBear.RaiseTestBear'>",
    "<class 'RaiseTestBear.RaiseTestExecuteBear'>",
    "<class 'TestBear.TestBear'>",
    "<class 'TestBearDep.TestDepBearA'>",
    "<class 'TestBearDep.TestDepBearAA'>",
    "<class 'TestBearDep.TestDepBearBDependsA'>",
    "<class 'TestBearDep.TestDepBearCDependsB'>",
    "<class 'TestBearDep.TestDepBearDependsAAndAA'>",
    "<class 'DependentBear.DependentBear'>",
    "<class 'SpaceConsistencyTestBear.SpaceConsistencyTestBear'>",
]


def execute_coala(func, binary, *args, debug=False):
    """
    Executes the main function with the given argument string from given module.

    :param function:    A main function from coala_json, coala_ci module etc.
    :param binary:      A binary to execute coala test
    :param debug:       Run main function with ``debug=True`` and re-raise any
                        exception coming back.
    :return:            A tuple holding a return value as first element,
                        a stdout output as second element and a stderr output
                        as third element if stdout_only is False.
    """
    sys.argv = [binary] + list(args)
    with retrieve_stdout() as stdout:
        with retrieve_stderr() as stderr:
            retval = func(debug=debug)
            return (retval, stdout.getvalue(), stderr.getvalue())


@contextmanager
def bear_test_module():
    """
    This function mocks the ``pkg_resources.iter_entry_points()``
    to use the testing bear module we have. Hence, it doesn't test
    the collection of entry points.
    """
    bears_test_module = os.path.join(os.path.dirname(__file__),
                                     'test_bears', '__init__.py')

    class EntryPoint:

        @staticmethod
        def load():
            class PseudoPlugin:
                __file__ = bears_test_module
            return PseudoPlugin()

    with unittest.mock.patch('pkg_resources.iter_entry_points',
                             return_value=[EntryPoint()]) as mocked:
        yield
