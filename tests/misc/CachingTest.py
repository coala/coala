import unittest
import os
from unittest.mock import patch

from pyprint.NullPrinter import NullPrinter

from coalib.misc.Caching import FileCache
from coalib.misc.CachingUtilities import pickle_load, pickle_dump
from coalib.output.printers.LogPrinter import LogPrinter
from coalib import coala


class CachingTest(unittest.TestCase):

    def setUp(self):
        current_dir = os.path.split(__file__)[0]
        self.caching_test_dir = os.path.join(
            current_dir,
            "caching_testfiles")
        self.log_printer = LogPrinter(NullPrinter())
        self.cache = FileCache(self.log_printer, "coala_test", flush_cache=True)

    def test_file_tracking(self):
        self.cache.track_files({"test.c", "file.py"})
        self.assertEqual(self.cache.data, {"test.c": -1, "file.py": -1})

        self.cache.untrack_files({"test.c"})
        self.assertFalse("test.c" in self.cache.data)
        self.assertTrue("file.py" in self.cache.data)

        self.cache.untrack_files({"test.c", "file.py"})
        self.assertFalse("test.c" in self.cache.data)
        self.assertFalse("file.py" in self.cache.data)

    def test_write(self):
        self.cache.track_files({"test2.c"})
        self.assertEqual(self.cache.data["test2.c"], -1)

        self.cache.write()
        self.assertNotEqual(self.cache.data["test2.c"], -1)

    @patch('coalib.misc.Caching.os')
    def test_get_uncached_files(self, mock_os):
        file_path = os.path.join(self.caching_test_dir, "test.c")
        cache = FileCache(self.log_printer, "coala_test3", flush_cache=True)

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
        with FileCache(self.log_printer, "test3", flush_cache=True) as cache:
            cache.track_files({"file.c"})
        self.assertTrue("file.c" in cache.data)

        with FileCache(self.log_printer, "test3", flush_cache=False) as cache:
            self.assertTrue("file.c" in cache.data)

    def test_time_travel(self):
        cache = FileCache(self.log_printer, "coala_test2", flush_cache=True)
        cache.track_files({"file.c"})
        cache.write()
        self.assertTrue("file.c" in cache.data)

        cache_data = pickle_load(self.log_printer, "coala_test2", {})
        # Back to the future :)
        cache_data["time"] = 2000000000
        pickle_dump(self.log_printer, "coala_test2", cache_data)

        cache = FileCache(self.log_printer, "coala_test2", flush_cache=False)
        self.assertFalse("file.c" in cache.data)
