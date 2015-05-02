import glob as python_standard_glob
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, ".")
from coalib.parsing.Glob import glob, iglob, _Selector, _iter_or_combinations


class GlobTest(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp(prefix='coala_import_test_dir_')
        self.tmp_subdir = tempfile.mkdtemp(prefix='pref',
                                           dir=self.tmp_dir)
        self.tmp_subdir2 = tempfile.mkdtemp(prefix='random',
                                            dir=self.tmp_subdir)
        self.tmp_subdir3 = tempfile.mkdtemp(prefix='random2',
                                            dir=self.tmp_subdir2)
        (self.testfile1, self.testfile1_path) = tempfile.mkstemp(
            suffix='.py',
            prefix='testfile1_',
            dir=self.tmp_subdir2)
        (self.testfile2, self.testfile2_path) = tempfile.mkstemp(
            suffix='.c',
            prefix='testfile2_',
            dir=self.tmp_subdir2)
        (self.testfile3, self.testfile3_path) = tempfile.mkstemp(
            suffix='.py',
            prefix='testfile3_',
            dir=self.tmp_subdir3)
        # We don't need the file opened
        os.close(self.testfile1)
        os.close(self.testfile2)
        os.close(self.testfile3)

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    def test_files(self):
        file_name_list = sorted(glob(os.path.join(self.tmp_dir,
                                                  "pref*",
                                                  "**",
                                                  "*.py"),
                                     dirs=False))
        self.assertEqual(file_name_list,
                         sorted([self.testfile1_path, self.testfile3_path]))

    def test_dirs(self):
        dir_name_list = sorted(glob(os.path.join(self.tmp_dir,
                                                 "**",
                                                 "random*"),
                                    files=False))
        self.assertEqual(dir_name_list,
                         sorted([self.tmp_subdir2, self.tmp_subdir3]))

    def test_no_dirs(self):
        dir_name_list = sorted(glob(os.path.join(self.tmp_dir,
                                                 "**",
                                                 "random*"),
                                    dirs=False))
        self.assertEqual(dir_name_list, [])

    def test_or(self):
        file_name_list = sorted(glob(os.path.join(self.tmp_dir, "pref*", "**",
                                                  "*(.py|.c)"), dirs=False))
        self.assertEqual(file_name_list,
                         sorted([self.testfile1_path,
                                 self.testfile2_path,
                                 self.testfile3_path]))

    def test_miss(self):
        dir_name_list = sorted(glob(os.path.join("*",
                                                 "something",
                                                 "that",
                                                 "isnt",
                                                 "there")))
        self.assertEqual(dir_name_list, [])

    def test_none(self):
        dir_name_list = sorted(glob(os.path.join(self.tmp_dir, "**", "*"),
                                    files=False,
                                    dirs=False))
        self.assertEqual(dir_name_list, [])

    def test_empty(self):
        self.assertEqual(glob(""), [])

    def test_random(self):
        path = os.path.join(os.getcwd(), "*", "*.py")
        self.assertTrue(self.matches_standard_glob(glob(path), path))

    def test_curdir(self):
        self.assertTrue(self.matches_standard_glob(glob("*"), "*"))

    def test_wrong_wildcard(self):
        with self.assertRaises(ValueError):
            list(iglob(os.path.join("**", "a**b", "**")))

    def test_selector_error(self):
        with self.assertRaises(NotImplementedError):
            a = _Selector(False)
            a._collect("stuff")

    def matches_standard_glob(self, file_list, pattern):
        file_list = sorted(file_list)
        glob_list = python_standard_glob.glob(pattern)
        if pattern.startswith('*'):
            glob_list.extend(python_standard_glob.glob('.' + pattern))
        absolute_glob_list = [os.path.abspath(path) for path in glob_list]
        return file_list == sorted(absolute_glob_list)


class IterOrCombinationTest(unittest.TestCase):
    def test_correct_evaluation(self):
        pattern_result_dict = {
            "": [""],
            "()": [""],
            "()()()()()": [""],
            "()((()))(())": [""],
            "abc": ["abc"],
            "(a)": ["a"],
            "(|)": [""],
            "(a|)": ["", "a"],
            "(a|b)": ["a", "b"],
            "(a)(b)(c)": ["abc"],
            "a(b|c)d": ["abd", "acd"],
            "(a(b|c)d)": ["abd", "acd"],
            "((a|b)|c|d)": ["a", "b", "c", "d"],
            "(a|b)(c|d)": ["ac", "ad", "bc", "bd"],
            "a((b|c|d)|e(f|g))(h|i)j": ["abhj",
                                        "abij",
                                        "achj",
                                        "acij",
                                        "adhj",
                                        "adij",
                                        "aefhj",
                                        "aefij",
                                        "aeghj",
                                        "aegij"]
            }

        for pattern, result_list in pattern_result_dict.items():
            self.assertEqual(sorted(list(_iter_or_combinations(pattern))),
                             result_list)

    def test_parentheses_check(self):
        pattern_list = ["(",
                        ")",
                        "())",
                        "(()",
                        "a(b|(c)d",
                        "ab|(c)d(",
                        ")(",
                        "())("
                        "a((b|c|d)|e)(f|g))(h|i)j"]

        for pattern in pattern_list:
            self.assertRaises(ValueError, list, _iter_or_combinations(pattern))

    def test_long_delimiters(self):
        pattern = "AAAAAAaBBBbCCCAAAcBBBdCCCBBBeCCC"  # ((a|b)(c|d)|e)
        result_list = ["ac", "ad", "bc", "bd", "e"]
        self.assertEqual(
            sorted(list(_iter_or_combinations(pattern,
                                              opening_delimiter="AAA",
                                              closing_delimiter="CCC",
                                              separator="BBB"))),
            result_list)

    def test_long_delimiter_check(self):
        pattern = "AAAAAAaBBBbCCCAAAcBBBAAAdCCCBBBeCCC"  # ((a|b)(c|(d)|e)
        self.assertRaises(ValueError,
                          list,
                          _iter_or_combinations(pattern,
                                                opening_delimiter="AAA",
                                                closing_delimiter="CCC",
                                                separator="BBB"))

if __name__ == '__main__':
    unittest.main(verbosity=2)
