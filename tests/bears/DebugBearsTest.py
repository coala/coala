import unittest
import sys

from io import StringIO

from coalib.bears.Bear import Debugger, debug_run


def func1(*args, **kwargs):
    yield 1
    yield 2
    yield 3


def func2(*args, **kwargs):
    return [1, 2]


def func3(*args, **kwargs):
    return func1(*args, **kwargs)


def execute_debugger(debugger_commands, func, *args, **kwargs):
    input = StringIO('\n'.join(debugger_commands))
    output = StringIO()
    dbg = Debugger(stdin=input, stdout=output)
    return debug_run(func, dbg, *args, **kwargs), output.getvalue()


class DebugBearsTest(unittest.TestCase):
    def setUp(self):
        # restore the coverage settrace to prevent the coverage breakage
        # on project because we can't chain coverage trace to run parallel
        # with debugger. To increase the coverage Mock test has been added in
        # BearTest file.
        # https://goo.gl/sKaJfh
        self.trace = sys.gettrace()

    def tearDown(self):
        sys.settrace(self.trace)

    def test_run_return_yield_with_debugger(self):
        result, output = execute_debugger('qcqc', func1)
        self.assertEqual(result, [1, 2, 3])
        lines = output.splitlines()
        self.assertEqual(lines[1], '-> yield 1')
        self.assertEqual(lines[3], '-> yield 2')
        self.assertEqual(lines[5], '-> yield 3')

    def test_run_return_list_with_debugger(self):
        result, output = execute_debugger('q', func2)
        self.assertEqual(result, [1, 2])
        lines = output.splitlines()
        self.assertEqual(lines[1], '-> return [1, 2]')

    def test_run_return_generator_with_debugger(self):
        result, output = execute_debugger('qcqcq', func3)
        self.assertEqual(result, [1, 2, 3])
        lines = output.splitlines()
        self.assertEqual(lines[3], '-> yield 1')
        self.assertEqual(lines[5], '-> yield 2')
        self.assertEqual(lines[7], '-> yield 3')
