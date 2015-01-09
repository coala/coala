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
from coalib.misc.StringConstants import StringConstants
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting
from coalib.collecting.BearCollector import BearCollector


class TestInit(unittest.TestCase):
    def test_raises(self):
        self.assertRaises(TypeError, BearCollector, bear_kinds=5)
        self.assertRaises(TypeError, BearCollector, bear_kinds=[], flat_bear_dirs=5)
        self.assertRaises(TypeError, BearCollector, bear_kinds=[], rec_bear_dirs=5)
        self.assertRaises(TypeError, BearCollector, bear_kinds=[], bear_names=5)
        self.assertRaises(TypeError, BearCollector, bear_kinds=[], ignored_bears=5)
        self.assertRaises(TypeError, BearCollector, bear_kinds=[], regex=5)
        self.assertRaises(TypeError, BearCollector, bear_kinds=[], log_printer=5)

        self.assertEqual(BearCollector(["kind"])._regex, "$")

    def test_from_section(self):
        self.assertRaises(TypeError, BearCollector.from_section, ["kind"], 5)

        test_section = Section("test")
        test_section.append(Setting("flat_bear_dirs", ""))
        test_section.append(Setting("rec_bear_dirs", "test value"))
        test_section.append(Setting("bears", "test value"))
        test_section.append(Setting("bears_regex", "test value"))
        test_section.append(Setting("ignored_bear_dirs", "test value"))

        uut = BearCollector.from_section(["kind"], test_section)

        uut._prelim_flat_dirs = [StringConstants.coalib_bears_root]


class TestFileCollection(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp(prefix='coala_import_test_dir_')
        self.parent_from_tmp = os.path.abspath(os.path.join(self.tmp_dir, os.path.pardir))
        (self.testfile1, self.testfile1_path) = tempfile.mkstemp(suffix='.py', prefix='testfile1_', dir=self.tmp_dir)
        (self.testfile2, self.testfile2_path) = tempfile.mkstemp(suffix='.py', prefix='testfile2_', dir=self.tmp_dir)
        (self.testfile3, self.testfile3_path) = tempfile.mkstemp(suffix='.c', prefix='testfile3_', dir=self.tmp_dir)
        # We don't use the file descriptors
        os.close(self.testfile1)
        os.close(self.testfile2)
        os.close(self.testfile3)
        first_file_name = os.path.splitext(os.path.basename(self.testfile1_path))[0]
        test_bear_file_string_one = """
from coalib.bears.Bear import Bear
import inspect
import multiprocessing
from coalib.settings.Section import Section

class TestBear(Bear):
    def __init__(self):
        Bear.__init__(self, Section("settings"), multiprocessing.Queue())

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
                            flat_bear_dirs=[self.tmp_dir],
                            regex=".*")
        bear_list = uut.collect()
        self.assertEqual(len(bear_list), 2)
        self.assertTrue([bear_class().origin() for bear_class in bear_list]
                        in
                        [list(Tuple) for Tuple in itertools.permutations([self.testfile1_path, self.testfile2_path])])

    def test_bear_names(self):
        uut = BearCollector(["kind"],
                            flat_bear_dirs=[self.tmp_dir],
                            bear_names=[os.path.splitext(os.path.basename(self.testfile1_path))[0]])
        bear_list = uut.collect()
        self.assertEqual(len(bear_list), 1)
        self.assertEqual(bear_list[0]().origin(), self.testfile1_path)

        uut = BearCollector(["kind"],
                            flat_bear_dirs=[self.tmp_dir])
        bear_list = uut.collect()
        self.assertEqual(len(bear_list), 0)

    def test_ignored(self):
        uut = BearCollector(["kind"],
                            flat_bear_dirs=[self.tmp_dir],
                            ignored_bears=[os.path.splitext(os.path.basename(self.testfile1_path))[0]],
                            regex=".*")
        bear_list = uut.collect()
        self.assertEqual(len(bear_list), 1)
        self.assertEqual(bear_list[0]().origin(), self.testfile2_path)

    def test_regexs(self):
        uut = BearCollector(["kind"],
                            flat_bear_dirs=[self.parent_from_tmp],
                            regex="testfile1.*")
        bear_list = uut.collect()
        self.assertEqual(len(bear_list), 0)

        uut = BearCollector(["kind"],
                            rec_bear_dirs=[self.parent_from_tmp],
                            regex="testfile1")
        bear_list = uut.collect()
        self.assertEqual(len(bear_list), 0)

        uut = BearCollector(["kind"],
                            rec_bear_dirs=[self.parent_from_tmp],
                            regex="testfile1.*")
        bear_list = uut.collect()
        self.assertEqual(len(bear_list), 1)
        self.assertEqual(bear_list[0]().origin(), self.testfile1_path)

        uut = BearCollector(["kind"],
                            rec_bear_dirs=[self.parent_from_tmp],
                            regex="^testfile1.*$")
        bear_list = uut.collect()
        self.assertEqual(len(bear_list), 1)
        self.assertEqual(bear_list[0]().origin(), self.testfile1_path)

    def test_bear_dir_ignoration(self):
        uut = BearCollector(["kind"],
                            rec_bear_dirs=[self.parent_from_tmp],
                            ignored_bear_dirs=[self.tmp_dir],
                            regex="testfile1.*")
        bear_list = uut.collect()
        self.assertEqual(len(bear_list), 0)

        uut = BearCollector(["kind"],
                            rec_bear_dirs=[self.parent_from_tmp],
                            ignored_bear_dirs=[self.parent_from_tmp],
                            regex="testfile1.*")
        bear_list = uut.collect()
        self.assertEqual(len(bear_list), 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
