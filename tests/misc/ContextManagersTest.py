import os
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from coala_utils.ContextManagers import (
    change_directory, make_temp, prepare_file, retrieve_stdout,
    retrieve_stderr, simulate_console_inputs, subprocess_timeout,
    suppress_stdout)
from coalib.processes.Processing import create_process_group


process_group_timeout_test_code = """
import time, subprocess, sys;
p = subprocess.Popen([sys.executable,
                     "-c",
                     "import time; time.sleep(100)"]);
time.sleep(100);
"""


class ContextManagersTest(unittest.TestCase):

    def test_subprocess_timeout(self):
        p = subprocess.Popen([sys.executable,
                              '-c',
                              'import time; time.sleep(0.5);'],
                             stderr=subprocess.PIPE)
        with subprocess_timeout(p, 0.2) as timedout:
            retval = p.wait()
            p.stderr.close()
            self.assertEqual(timedout.value, True)
        self.assertNotEqual(retval, 0)

        p = create_process_group([sys.executable,
                                  '-c',
                                  process_group_timeout_test_code])
        with subprocess_timeout(p, 0.5, kill_pg=True):
            retval = p.wait()
            self.assertEqual(timedout.value, True)
        self.assertNotEqual(retval, 0)

        p = subprocess.Popen([sys.executable,
                              '-c',
                              'import time'])
        with subprocess_timeout(p, 0.5) as timedout:
            retval = p.wait()
            self.assertEqual(timedout.value, False)
        self.assertEqual(retval, 0)

        p = subprocess.Popen([sys.executable,
                              '-c',
                              'import time'])
        with subprocess_timeout(p, 0) as timedout:
            retval = p.wait()
            self.assertEqual(timedout.value, False)
        self.assertEqual(retval, 0)

    def test_suppress_stdout(self):
        def print_func():
            print('func')
            raise NotImplementedError

        def no_print_func():
            with suppress_stdout():
                print('func')
                raise NotImplementedError

        old_stdout = sys.stdout
        sys.stdout = False

        self.assertRaises(AttributeError, print_func)
        self.assertRaises(NotImplementedError, no_print_func)

        sys.stdout = old_stdout

    def test_retrieve_stdout(self):
        with retrieve_stdout() as sio:
            print('test', file=sys.stdout)
            self.assertEqual(sio.getvalue(), 'test\n')

    def test_retrieve_stderr(self):
        with retrieve_stderr() as sio:
            print('test', file=sys.stderr)
            self.assertEqual(sio.getvalue(), 'test\n')

    def test_simulate_console_inputs(self):
        with simulate_console_inputs(0, 1, 2) as generator:
            self.assertEqual(input(), 0)
            self.assertEqual(generator.last_input, 0)
            generator.inputs.append(3)
            self.assertEqual(input(), 1)
            self.assertEqual(input(), 2)
            self.assertEqual(input(), 3)
            self.assertEqual(generator.last_input, 3)

        with simulate_console_inputs('test'), self.assertRaises(ValueError):
            self.assertEqual(input(), 'test')
            input()

    def test_make_temp(self):
        with make_temp() as f_a:
            self.assertTrue(os.path.isfile(f_a))
            self.assertTrue(os.path.basename(f_a).startswith('tmp'))
        self.assertFalse(os.path.isfile(f_a))

        with make_temp(suffix='.orig', prefix='pre') as f_b:
            self.assertTrue(f_b.endswith('.orig'))
            self.assertTrue(os.path.basename(f_b).startswith('pre'))

    def test_prepare_file(self):
        with prepare_file(['line1', 'line2\n'],
                          '/file/name',
                          force_linebreaks=True,
                          create_tempfile=True) as (lines, filename):
            self.assertEqual(filename, '/file/name')
            self.assertEqual(lines, ['line1\n', 'line2\n'])

        with prepare_file(['line1', 'line2\n'],
                          None,
                          force_linebreaks=False,
                          create_tempfile=True) as (lines, filename):
            self.assertTrue(os.path.isfile(filename))
            self.assertEqual(lines, ['line1', 'line2\n'])

        with prepare_file(['line1', 'line2\n'],
                          None,
                          tempfile_kwargs={'suffix': '.test',
                                           'prefix': 'test_'},
                          force_linebreaks=False,
                          create_tempfile=True) as (lines, filename):
            self.assertTrue(os.path.isfile(filename))
            basename = os.path.basename(filename)
            self.assertTrue(basename.endswith('.test'))
            self.assertTrue(basename.startswith('test_'))

        with prepare_file(['line1', 'line2\n'],
                          None,
                          force_linebreaks=False,
                          create_tempfile=False) as (lines, filename):
            self.assertEqual(filename, 'dummy_file_name')

    def test_change_directory(self):
        old_dir = os.getcwd()
        with TemporaryDirectory('temp') as tempdir:
            tempdir = os.path.realpath(tempdir)
            with change_directory(tempdir):
                self.assertEqual(os.getcwd(), tempdir)
        self.assertEqual(os.getcwd(), old_dir)
