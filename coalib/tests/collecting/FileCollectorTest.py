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
import imp
import os
import shutil
import sys
import tempfile
sys.path.insert(0, ".")
import unittest
from coalib.collecting.FileCollector import FileCollector
from coalib.output.LogPrinter import LogPrinter


class TestInit(unittest.TestCase):
    def setUp(self):
        self.lp = LogPrinter()

    def test_raises(self):
        self.assertRaises(TypeError, FileCollector, "not a log_printer")
        self.assertRaises(TypeError, FileCollector, self.lp, "string", [], [], [], [])
        self.assertRaises(TypeError, FileCollector, self.lp, [], "string", [], [], [])
        self.assertRaises(TypeError, FileCollector, self.lp, [], [], "string", [], [])
        self.assertRaises(TypeError, FileCollector, self.lp, [], [], [], "string", [])
        self.assertRaises(TypeError, FileCollector, self.lp, [], [], [], [], "string")

    def test_members_empty(self):
        uut = FileCollector(self.lp)
        self.assertEqual(uut.log_printer, self.lp)
        self.assertEqual(uut._flat_dirs, [])
        self.assertEqual(uut._rec_dirs, [])
        self.assertEqual(uut._allowed, [])
        self.assertEqual(uut._forbidden, [])
        self.assertEqual(uut._ignored, [])

    def test_members_full(self):
        uut = FileCollector(self.lp, [os.getcwd()], ["abc", "xyz"], [".py", ".c"], [".h"], None)
        self.assertEqual(uut.log_printer, self.lp)
        self.assertEqual(uut._flat_dirs, [os.getcwd()])
        self.assertEqual(uut._rec_dirs, [os.path.abspath("abc"), os.path.abspath("xyz")])
        self.assertEqual(uut._allowed, [".py", ".c"])
        self.assertEqual(uut._forbidden, [".h"])
        self.assertEqual(uut._ignored, [])


class TestFileCollection(unittest.TestCase):
    def setUp(self):
        self.lp = LogPrinter()
        self.tmp_dir = tempfile.mkdtemp(prefix='coala_import_test_dir_')
        self.tmp_subdir = tempfile.mkdtemp(prefix='coala_import_test_subdir_', dir=self.tmp_dir)
        (self.testfile1, self.testfile1_path) = tempfile.mkstemp(suffix='.py', prefix='testfile1_', dir=self.tmp_dir)
        (self.testfile2, self.testfile2_path) = tempfile.mkstemp(suffix='.c', prefix='testfile2_', dir=self.tmp_dir)
        (self.testfile3, self.testfile3_path) = tempfile.mkstemp(suffix='.py', prefix='testfile3_', dir=self.tmp_subdir)

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    def test_flat(self):
        uut = FileCollector(self.lp, flat_dirs=[self.tmp_dir])
        self.assertEqual(set(uut.collect()), {self.testfile1_path, self.testfile2_path})

    def test_recursive(self):
        uut = FileCollector(self.lp, rec_dirs=[self.tmp_dir])
        self.assertEqual(set(uut.collect()), {self.testfile1_path, self.testfile2_path, self.testfile3_path})

    def test_allowed(self):
        uut = FileCollector(self.lp, rec_dirs=[self.tmp_dir], allowed=[".py"])
        self.assertEqual(set(uut.collect()), {self.testfile1_path, self.testfile3_path})

    def test_forbidden(self):
        uut = FileCollector(self.lp, rec_dirs=[self.tmp_dir], forbidden=[".c"])
        self.assertEqual(set(uut.collect()), {self.testfile1_path, self.testfile3_path})

    def test_ignored(self):
        uut = FileCollector(self.lp, rec_dirs=[self.tmp_dir], ignored=[self.testfile2_path])
        self.assertEqual(set(uut.collect()), {self.testfile1_path, self.testfile3_path})

    def test_nonexistent_directory(self):
        self.assertEqual(FileCollector(QuietPrinter(), flat_dirs=["bullshit"]).collect(), [])
        self.assertEqual(FileCollector(QuietPrinter(), rec_dirs=["bullshit"]).collect(), [])
        self.assertRaises(ZeroDivisionError, FileCollector(LoudPrinter(), flat_dirs=["bullshit"]).collect)
        self.assertRaises(ZeroDivisionError, FileCollector(LoudPrinter(), rec_dirs=["bullshit"]).collect)

    @unittest.skipIf(sys.version_info < (3, 3), "Mocks are not supported in Python 3.2")
    def test_unreadable_directory(self):
        from unittest.mock import MagicMock
        os.listdir = MagicMock(side_effect=OSError)
        self.assertEqual(FileCollector(QuietPrinter(), flat_dirs=[os.getcwd()]).collect(), [])
        self.assertEqual(FileCollector(QuietPrinter(), rec_dirs=[os.getcwd()]).collect(), [])
        self.assertRaises(ZeroDivisionError, FileCollector(LoudPrinter(), flat_dirs=["bullshit"]).collect)
        self.assertRaises(ZeroDivisionError, FileCollector(LoudPrinter(), rec_dirs=["bullshit"]).collect)
        imp.reload(os)


class QuietPrinter(LogPrinter):
    def __init__(self):
        LogPrinter.__init__(self)

    def warn(self, *args):
        pass


class LoudPrinter(LogPrinter):
    def __init__(self):
        LogPrinter.__init__(self)

    def warn(self, *args):
        raise ZeroDivisionError

if __name__ == '__main__':
    unittest.main(verbosity=2)
