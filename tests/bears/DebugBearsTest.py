import unittest
import sys

from io import StringIO
from queue import Queue

from coalib.bears.Bear import Bear, Debugger, debug_run
from coalib.bears.LocalBear import LocalBear
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


def func1(*args, **kwargs):
    yield 1
    yield 2
    yield 3


def func2(*args, **kwargs):
    return [1, 2]


def func3(*args, **kwargs):
    return func1(*args, **kwargs)


class TestOneBear(LocalBear):
    def __init__(self, section, queue):
        Bear.__init__(self, section, queue)

    def run(self, x: int, y: str, z: int = 79, w: str = 'kbc'):
        args = ()
        kwargs = {}
        return func1(*args, **kwargs)


def execute_debugger(debugger_commands, func, bear, *args, **kwargs):
    input = StringIO('\n'.join(debugger_commands))
    output = StringIO()
    dbg = Debugger(bear, stdin=input, stdout=output)
    return debug_run(func, dbg, *args, **kwargs), output.getvalue()


class DebugBearsTest(unittest.TestCase):
    def setUp(self):
        # restore the coverage settrace to prevent the coverage breakage
        # on project because we can't chain coverage trace to run parallel
        # with debugger. To increase the coverage Mock test has been added in
        # BearTest file.
        # https://goo.gl/sKaJfh
        self.trace = sys.gettrace()
        self.section = Section('name')
        self.queue = Queue()

    def tearDown(self):
        sys.settrace(self.trace)

    def test_run_return_yield_with_debugger(self):
        result, output = execute_debugger('qcqc', func1, bear=Bear(self.section,
                                                                   self.queue))
        self.assertEqual(result, [1, 2, 3])
        lines = output.splitlines()
        self.assertEqual(lines[1], '-> yield 1')
        self.assertEqual(lines[3], '-> yield 2')
        self.assertEqual(lines[5], '-> yield 3')

    def test_run_return_list_with_debugger(self):
        result, output = execute_debugger('q', func2, bear=Bear(self.section,
                                                                self.queue))
        self.assertEqual(result, [1, 2])
        lines = output.splitlines()
        self.assertEqual(lines[1], '-> return [1, 2]')

    def test_run_return_generator_with_debugger(self):
        result, output = execute_debugger('qcqcq', func3, bear=Bear(
            self.section, self.queue))
        self.assertEqual(result, [1, 2, 3])
        lines = output.splitlines()
        self.assertEqual(lines[3], '-> yield 1')
        self.assertEqual(lines[5], '-> yield 2')
        self.assertEqual(lines[7], '-> yield 3')

    def test_do_settings_with_bear_object(self):
        self.section.append(Setting('x', '85'))
        self.section.append(Setting('y', 'kbc3'))
        self.section.append(Setting('z', '75'))
        bear = TestOneBear(self.section, self.queue)
        kwargs = {'x': 2, 'y': 'abc'}
        result, output = execute_debugger(['q', 'c', 'settings', 'c', 'q', 'c'],
                                          bear.run, bear=bear, **kwargs)
        self.assertEqual(result, [1, 2, 3])
        lines = output.splitlines()
        self.assertEqual(lines[6], '(Pdb) x = 85')
        self.assertEqual(lines[7], "y = 'kbc3'")
        self.assertEqual(lines[8], 'z = 75')
        self.assertEqual(lines[9], "w = 'kbc'")

    def test_debugger_without_bear_object(self):
        with self.assertRaises(ValueError):
            execute_debugger([], func2, bear=None)
