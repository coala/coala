"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
import itertools
import os
import shutil
import sys
import tempfile
sys.path.insert(0, ".")
import unittest
from coalib.collecting.FilterCollector import FilterCollector
from coalib.output.LogPrinter import LogPrinter


class TestInit(unittest.TestCase):

    def test_raises(self):
        self.assertRaises(TypeError, FilterCollector, ["kind"], [], "string", [], [])
        self.assertRaises(TypeError, FilterCollector, ["kind"], [], [], "string", [])
        self.assertRaises(TypeError, FilterCollector, ["kind"], [], [], [], "string")
        self.assertRaises(TypeError, FilterCollector, "kind", [], [], [], [])

        self.assertEqual(FilterCollector(["kind"], [])._regexs, [])


class TestFileCollection(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp(prefix='coala_import_test_dir_')
        (self.testfile1, self.testfile1_path) = tempfile.mkstemp(suffix='.py', prefix='testfile1_', dir=self.tmp_dir)
        (self.testfile2, self.testfile2_path) = tempfile.mkstemp(suffix='.py', prefix='testfile2_', dir=self.tmp_dir)
        (self.testfile3, self.testfile3_path) = tempfile.mkstemp(suffix='.c', prefix='testfile3_', dir=self.tmp_dir)
        first_file_name = os.path.splitext(os.path.basename(self.testfile1_path))[0]
        test_filter_file_string_one = """
from coalib.bears.Bear import Bear
import inspect
import multiprocessing
from coalib.settings.Settings import Settings

class TestFilter(Bear):
    def __init__(self):
        Bear.__init__(self, Settings("settings"), multiprocessing.Queue())

    @staticmethod
    def kind():
        return "kind"

    def origin(self):
        return inspect.getfile(inspect.currentframe())


class NoKind():
    def __init__(self):
        pass

    @staticmethod
    def kind():
        raise NotImplementedError

"""
        test_filter_file_string_two = """
from {} import TestFilter as ImportedTestFilter
import inspect

class TestFilter(ImportedTestFilter):
    def __init__(self):
        ImportedTestFilter.__init__(self)

    @staticmethod
    def kind():
        return "kind"

    def origin(self):
        return inspect.getfile(inspect.currentframe())
""".format(first_file_name)
        with open(self.testfile1_path, 'w') as test_filter_file:
            test_filter_file.write(test_filter_file_string_one)
        with open(self.testfile2_path, 'w') as test_filter_file:
            test_filter_file.write(test_filter_file_string_two)
        with open(self.testfile3_path, 'w') as test_filter_file:
            test_filter_file.write(test_filter_file_string_one)

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    def test_filter_import(self):
        uut = FilterCollector(["kind"],
                              filter_dirs=[self.tmp_dir])
        filter_list = uut.collect()
        self.assertEqual(len(filter_list), 2)
        self.assertTrue([filter_class().origin() for filter_class in filter_list]
                        in
                        [list(Tuple) for Tuple in itertools.permutations([self.testfile1_path, self.testfile2_path])])

    def test_filter_names(self):
        uut = FilterCollector(["kind"],
                              filter_dirs=[self.tmp_dir],
                              filter_names=[os.path.splitext(os.path.basename(self.testfile1_path))[0]])
        filter_list = uut.collect()
        self.assertEqual(len(filter_list), 1)
        self.assertEqual(filter_list[0]().origin(), self.testfile1_path)

    def test_ignored(self):
        uut = FilterCollector(["kind"],
                              filter_dirs=[self.tmp_dir],
                              ignored_filters=[os.path.splitext(os.path.basename(self.testfile1_path))[0]])
        filter_list = uut.collect()
        self.assertEqual(len(filter_list), 1)
        self.assertEqual(filter_list[0]().origin(), self.testfile2_path)

    def test_regexs(self):
        uut = FilterCollector(["kind"],
                              filter_dirs=[self.tmp_dir],
                              regexs=["testfile1"])
        filter_list = uut.collect()
        print(filter_list)
        self.assertEqual(len(filter_list), 1)
        self.assertEqual(filter_list[0]().origin(), self.testfile1_path)

if __name__ == '__main__':
    unittest.main(verbosity=2)
