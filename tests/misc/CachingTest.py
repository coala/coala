import unittest
import re
import os
from unittest.mock import patch

from pyprint.NullPrinter import NullPrinter

from coalib.misc.Caching import FileCache
from coalib.misc.CachingUtilities import pickle_load, pickle_dump
from coalib.output.printers.LogPrinter import LogPrinter
from coalib import coala
from coala_utils.ContextManagers import prepare_file
from coala_utils.ContextManagers import simulate_console_inputs
from tests.TestUtilities import execute_coala, bear_test_module


class CachingTest(unittest.TestCase):

    def setUp(self):
        current_dir = os.path.split(__file__)[0]
        self.caching_test_dir = os.path.join(
            current_dir,
            'caching_testfiles')
        self.log_printer = LogPrinter(NullPrinter())
        self.cache = FileCache(self.log_printer, 'coala_test', flush_cache=True)

    def test_file_tracking(self):
        self.cache.track_files({'test.c', 'file.py'})
        self.assertEqual(self.cache.data, {'test.c': -1, 'file.py': -1})

        self.cache.untrack_files({'test.c'})
        self.cache.track_files({'test.c'})
        self.cache.write()
        self.assertFalse('test.c' in self.cache.data)
        self.assertTrue('file.py' in self.cache.data)

        self.cache.untrack_files({'test.c', 'file.py'})
        self.cache.write()
        self.assertFalse('test.c' in self.cache.data)
        self.assertFalse('file.py' in self.cache.data)

    def test_write(self):
        self.cache.track_files({'test2.c'})
        self.assertEqual(self.cache.data['test2.c'], -1)

        self.cache.write()
        self.assertNotEqual(self.cache.data['test2.c'], -1)

    @patch('coalib.misc.Caching.os')
    def test_get_uncached_files(self, mock_os):
        file_path = os.path.join(self.caching_test_dir, 'test.c')
        cache = FileCache(self.log_printer, 'coala_test3', flush_cache=True)

        # Since this is a new FileCache object, the return must be the full set
        cache.current_time = 0
        mock_os.path.getmtime.return_value = 0
        self.assertEqual(cache.get_uncached_files({file_path}), {file_path})

        cache.track_files({file_path})
        self.assertEqual(cache.get_uncached_files({file_path}), {file_path})

        cache.write()
        self.assertEqual(cache.get_uncached_files({file_path}), set())

        # Simulate changing the file and then getting uncached files
        # Since the file has been edited since the last run it's returned
        cache.current_time = 1
        mock_os.path.getmtime.return_value = 1
        cache.track_files({file_path})
        self.assertEqual(cache.get_uncached_files({file_path}), {file_path})
        cache.write()

        # Not changing the file should NOT return it the next time
        cache.current_time = 2
        self.assertEqual(cache.get_uncached_files({file_path}), set())

    def test_persistence(self):
        with FileCache(self.log_printer, 'test3', flush_cache=True) as cache:
            cache.track_files({'file.c'})
        self.assertTrue('file.c' in cache.data)

        with FileCache(self.log_printer, 'test3', flush_cache=False) as cache:
            self.assertTrue('file.c' in cache.data)

    def test_time_travel(self):
        cache = FileCache(self.log_printer, 'coala_test2', flush_cache=True)
        cache.track_files({'file.c'})
        cache.write()
        self.assertTrue('file.c' in cache.data)

        cache_data = pickle_load(self.log_printer, 'coala_test2', {})
        # Back to the future :)
        cache_data['time'] = 2000000000
        pickle_dump(self.log_printer, 'coala_test2', cache_data)

        cache = FileCache(self.log_printer, 'coala_test2', flush_cache=False)
        self.assertFalse('file.c' in cache.data)

    def test_caching_results(self):
        """
        A simple integration test to assert that results are not dropped
        when coala is ran multiple times with caching enabled.
        """
        with bear_test_module(), \
                prepare_file(['a=(5,6)'], None) as (lines, filename):
            with simulate_console_inputs('0'):
                retval, stdout, stderr = execute_coala(
                    coala.main,
                    'coala',
                    '-c', os.devnull,
                    '--disable-caching',
                    '--flush-cache',
                    '-f', re.escape(filename),
                    '-b', 'LineCountTestBear',
                    '-L', 'DEBUG')
                self.assertIn('This file has', stdout)
                self.assertIn('Running bear LineCountTestBear', stderr)

            # Due to the change in configuration from the removal of
            # ``--flush-cache`` this run will not be sufficient to
            # assert this behavior.
            retval, stdout, stderr = execute_coala(
                coala.main,
                'coala',
                '-c', os.devnull,
                '-f', re.escape(filename),
                '-b', 'LineCountTestBear')
            self.assertIn('This file has', stdout)
            self.assertIn(' During execution of coala', stderr)

            retval, stdout, stderr = execute_coala(
                coala.main,
                'coala',
                '-c', os.devnull,
                '-f', re.escape(filename),
                '-b', 'LineCountTestBear')
            self.assertIn('This file has', stdout)
            self.assertIn('During execution of coala', stderr)

    def test_caching_multi_results(self):
        """
        Integration test to assert that results are not dropped when coala is
        ran multiple times with caching enabled and one section yields a result
        and second one doesn't.
        """
        filename = 'tests/misc/test_caching_multi_results/'
        with bear_test_module():
            with simulate_console_inputs('0'):
                retval, stdout, stderr = execute_coala(
                   coala.main,
                   'coala',
                   '-c', filename + '.coafile',
                   '-f', filename + 'test.py')
                self.assertIn('This file has', stdout)
                self.assertIn(
                    'Implicit \'Default\' section inheritance is deprecated',
                    stderr)

            retval, stdout, stderr = execute_coala(
               coala.main,
               'coala',
               '-c', filename + '.coafile',
               '-f', filename + 'test.py')
            self.assertIn('This file has', stdout)
            self.assertIn('During execution of coala', stderr)
            self.assertIn(
                'Implicit \'Default\' section inheritance is deprecated',
                stderr)
