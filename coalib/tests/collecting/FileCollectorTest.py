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

import os
import shutil
import sys
import tempfile

sys.path.insert(0, ".")
import unittest
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting
from coalib.collecting.FileCollector import FileCollector
from coalib.output.LogPrinter import LogPrinter


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


class TestInit(unittest.TestCase):
    def setUp(self):
        self.lp = LogPrinter()

    def test_raises(self):
        self.assertRaises(TypeError, FileCollector, log_printer="not a log_printer")
        self.assertRaises(TypeError, FileCollector, "string", [], [], [], [], [])
        self.assertRaises(TypeError, FileCollector, [], "string", [], [], [], [])
        self.assertRaises(TypeError, FileCollector, [], [], "string", [], [], [])
        self.assertRaises(TypeError, FileCollector, [], [], [], "string", [], [])
        self.assertRaises(TypeError, FileCollector, [], [], [], [], "string", [])
        self.assertRaises(TypeError, FileCollector, [], [], [], [], [], "string")

    def test_members_empty(self):
        uut = FileCollector(log_printer=self.lp)
        uut._unfold_params()
        self.assertEqual(uut.log_printer, self.lp)
        self.assertEqual(uut._flat_dirs, [])
        self.assertEqual(uut._rec_dirs, [])
        self.assertEqual(uut._allowed_types, None)
        self.assertEqual(uut._ignored_dirs, [])
        self.assertEqual(uut._ignored_files, [])

    def test_members_full(self):
        uut = FileCollector([], [os.getcwd()], ["abc", "xyz"], [".PY", "c"], [], [], log_printer=self.lp)
        uut._unfold_params()
        self.assertEqual(uut.log_printer, self.lp)
        self.assertEqual(uut._flat_dirs, [os.getcwd()])
        self.assertEqual(uut._rec_dirs, [os.path.abspath("abc"), os.path.abspath("xyz")])
        self.assertEqual(uut._allowed_types, ["py", "c"])
        self.assertEqual(uut._ignored_files, [])
        self.assertEqual(uut._ignored_dirs, [])

    def test_ignored_members(self):
        uut = FileCollector([], ["flat"], ["rec"], [], [], ["flat", "rec"])
        uut._unfold_params()
        self.assertEqual(uut._flat_dirs, [])
        self.assertEqual(uut._rec_dirs, [])

    def test_from_section(self):
        self.assertRaises(TypeError, FileCollector.from_section, 5)

        test_section = Section("test")
        test_section.append(Setting("files", "test value"))
        test_section.append(Setting("flat_dirs", "test value"))
        test_section.append(Setting("rec_dirs", "test value"))
        test_section.append(Setting("ignored_dirs", "test value"))

        FileCollector.from_section(test_section)


class TestFileCollection(unittest.TestCase):
    def setUp(self):
        self.lp = LogPrinter()
        self.tmp_dir = tempfile.mkdtemp(prefix='coala_import_test_dir_')
        self.tmp_subdir = tempfile.mkdtemp(prefix='coala_import_test_subdir_', dir=self.tmp_dir)
        (self.testfile1, self.testfile1_path) = tempfile.mkstemp(suffix='.py', prefix='testfile1_', dir=self.tmp_dir)
        (self.testfile2, self.testfile2_path) = tempfile.mkstemp(suffix='.c', prefix='testfile2_', dir=self.tmp_dir)
        (self.testfile3, self.testfile3_path) = tempfile.mkstemp(suffix='.py', prefix='testfile3_', dir=self.tmp_subdir)
        # We don't need the file opened
        os.close(self.testfile1)
        os.close(self.testfile2)
        os.close(self.testfile3)

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    def test_files(self):
        uut = FileCollector(files=["not_a_file", self.testfile1_path])
        self.assertEqual(set(uut.collect()), {self.testfile1_path})
        # Consecutive invocations shall be idempotent
        self.assertEqual(set(uut.collect()), {self.testfile1_path})

    def test_flat(self):
        uut = FileCollector(flat_dirs=[self.tmp_dir], log_printer=self.lp)
        self.assertEqual(set(uut.collect()), {self.testfile1_path, self.testfile2_path})

    def test_recursive(self):
        uut = FileCollector(rec_dirs=[self.tmp_dir], log_printer=self.lp)
        self.assertEqual(set(uut.collect()), {self.testfile1_path, self.testfile2_path, self.testfile3_path})

    def test_allowed(self):
        uut = FileCollector(rec_dirs=[self.tmp_dir], allowed_types=[".py"], log_printer=self.lp)
        self.assertEqual(set(uut.collect()), {self.testfile1_path, self.testfile3_path})

    def test_ignored_files(self):
        uut = FileCollector(rec_dirs=[self.tmp_dir], ignored_files=[self.testfile2_path], log_printer=self.lp)
        self.assertEqual(set(uut.collect()), {self.testfile1_path, self.testfile3_path})

    def test_nonexistent_directory(self):
        self.assertEqual(FileCollector(log_printer=QuietPrinter(), flat_dirs=["bullshit"]).collect(), [])
        self.assertEqual(FileCollector(log_printer=QuietPrinter(), rec_dirs=["bullshit"]).collect(), [])
        self.assertRaises(ZeroDivisionError, FileCollector(log_printer=LoudPrinter(), flat_dirs=["bullshit"]).collect)
        self.assertRaises(ZeroDivisionError,
                          FileCollector(log_printer=LoudPrinter(), rec_dirs=["bullshit"]).collect)

    @unittest.skipIf(sys.version_info < (3, 3), "Mocks are not supported in Python 3.2")
    def test_unreadable_directory(self):
        if sys.version_info < (3, 4):
            import imp as importlib
        else:
            import importlib
        from unittest.mock import MagicMock

        os.listdir = MagicMock(side_effect=OSError)
        self.assertEqual(FileCollector(log_printer=QuietPrinter(), flat_dirs=[os.getcwd()]).collect(), [])
        self.assertEqual(FileCollector(log_printer=QuietPrinter(), rec_dirs=[os.getcwd()]).collect(), [])
        self.assertRaises(ZeroDivisionError, FileCollector(log_printer=LoudPrinter(), flat_dirs=["bullshit"]).collect)
        self.assertRaises(ZeroDivisionError,
                          FileCollector(log_printer=LoudPrinter(), rec_dirs=["bullshit"]).collect)
        importlib.reload(os)


if __name__ == '__main__':
    unittest.main(verbosity=2)
