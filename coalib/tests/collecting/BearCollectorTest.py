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
from coalib.collecting.BearCollector import BearCollector


class TestInit(unittest.TestCase):
    def test_raises(self):
        self.assertRaises(TypeError, BearCollector, ["kind"], [], "string", [], [])
        self.assertRaises(TypeError, BearCollector, ["kind"], [], [], "string", [])
        self.assertRaises(TypeError, BearCollector, ["kind"], [], [], [], "string")
        self.assertRaises(TypeError, BearCollector, "kind", [], [], [], [])

        self.assertEqual(BearCollector(["kind"], [])._regexs, [])


class TestFileCollection(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp(prefix='coala_import_test_dir_')
        (self.testfile1, self.testfile1_path) = tempfile.mkstemp(suffix='.py', prefix='testfile1_', dir=self.tmp_dir)
        (self.testfile2, self.testfile2_path) = tempfile.mkstemp(suffix='.py', prefix='testfile2_', dir=self.tmp_dir)
        (self.testfile3, self.testfile3_path) = tempfile.mkstemp(suffix='.c', prefix='testfile3_', dir=self.tmp_dir)
        first_file_name = os.path.splitext(os.path.basename(self.testfile1_path))[0]
        test_bear_file_string_one = """
from coalib.bears.Bear import Bear
import inspect
import multiprocessing
from coalib.settings.Settings import Settings

class TestBear(Bear):
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
        test_bear_file_string_two = """
from {} import TestBear as ImportedTestBear
import inspect

class TestBear(ImportedTestBear):
    def __init__(self):
        ImportedTestBear.__init__(self)

    @staticmethod
    def kind():
        return "kind"

    def origin(self):
        return inspect.getfile(inspect.currentframe())
""".format(first_file_name)
        with open(self.testfile1_path, 'w') as test_bear_file:
            test_bear_file.write(test_bear_file_string_one)
        with open(self.testfile2_path, 'w') as test_bear_file:
            test_bear_file.write(test_bear_file_string_two)
        with open(self.testfile3_path, 'w') as test_bear_file:
            test_bear_file.write(test_bear_file_string_one)

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    def test_bear_import(self):
        uut = BearCollector(["kind"],
                            bear_dirs=[self.tmp_dir])
        bear_list = uut.collect()
        self.assertEqual(len(bear_list), 2)
        self.assertTrue([bear_class().origin() for bear_class in bear_list]
                        in
                        [list(Tuple) for Tuple in itertools.permutations([self.testfile1_path, self.testfile2_path])])

    def test_bear_names(self):
        uut = BearCollector(["kind"],
                            bear_dirs=[self.tmp_dir],
                            bear_names=[os.path.splitext(os.path.basename(self.testfile1_path))[0]])
        bear_list = uut.collect()
        self.assertEqual(len(bear_list), 1)
        self.assertEqual(bear_list[0]().origin(), self.testfile1_path)

    def test_ignored(self):
        uut = BearCollector(["kind"],
                            bear_dirs=[self.tmp_dir],
                            ignored_bears=[os.path.splitext(os.path.basename(self.testfile1_path))[0]])
        bear_list = uut.collect()
        self.assertEqual(len(bear_list), 1)
        self.assertEqual(bear_list[0]().origin(), self.testfile2_path)

    def test_regexs(self):
        uut = BearCollector(["kind"],
                            bear_dirs=[self.tmp_dir],
                            regexs=["testfile1"])
        bear_list = uut.collect()
        print(bear_list)
        self.assertEqual(len(bear_list), 1)
        self.assertEqual(bear_list[0]().origin(), self.testfile1_path)


if __name__ == '__main__':
    unittest.main(verbosity=2)
