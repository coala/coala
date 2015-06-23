import glob as python_standard_glob
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, ".")
from coalib.parsing.Globbing import (glob,
                                     iglob,
                                     _Selector,
                                     _iter_or_combinations)
from coalib.parsing.Globbing import _iter_alternatives
from coalib.parsing.Globbing import _iter_choices
from coalib.parsing.Globbing import _position_is_bracketed
from coalib.parsing.Globbing import fnmatch


class GlobbingHelperFunctionsTest(unittest.TestCase):
    def test_positions(self):
        # pattern: [bracketed values]
        pattern_positions_dict = {
            "[]": [],
            "[a]": [1],
            "[][]": [1, 2],
            "[]]]": [1],
            "[[[]": [1, 2],
            "[[[][]]]": [1, 2, 5],
            "][": [],
            "][][": [],
            "[!]": [],
            "[!c]": [1, 2],
            "[!": []
            }
        for pattern, bracketed_positions in pattern_positions_dict.items():
            for pos in range(len(pattern)):
                if pos in bracketed_positions:
                    self.assertTrue(_position_is_bracketed(pattern, pos))
                else:
                    self.assertFalse(_position_is_bracketed(pattern, pos))

    def test_choices(self):
        # pattern: [choices]
        pattern_choices_dict = {
            "": [""],
            "a": ["a"],
            "a|b": ["a", "b"],
            "a|b|c": ["a", "b", "c"],
            "a|b[|]c": ["a", "b[|]c"],
            "a|[b|c]": ["a", "[b|c]"],
            "a[|b|c]": ["a[|b|c]"],
            "[a|b|c]": ["[a|b|c]"],
            "[a]|[b]|[c]": ["[a]", "[b]", "[c]"],
            "[[a]|[b]|[c]": ["[[a]", "[b]", "[c]"]
            }
        for pattern, choices in pattern_choices_dict.items():
            self.assertEqual(list(_iter_choices(pattern)), choices)

    def test_alternatives(self):
        # pattern: [alternatives]
        pattern_alternatives_dict = {
            "": [""],
            "(ab)": ["ab"],
            "a|b": ["a|b"],
            "()": [""],
            "(|)": [""],
            "(a|b)": ["a", "b"],
            "(a|b|c)": ["a", "b", "c"],
            "a(b|c)": ["ab", "ac"],
            "(a|b)(c|d)": ["ac", "ad", "bc", "bd"],
            "(a|b(c|d)": ["(a|bc", "(a|bd"],
            "(a[|]b)": ["a[|]b"],
            "[(]a|b)": ["[(]a|b)"],
            }
        for pattern, alternatives in pattern_alternatives_dict.items():
            self.assertEqual(sorted(list(_iter_alternatives(pattern))),
                             sorted(alternatives))


class FnmatchTest(unittest.TestCase):
    def _test_fnmatch(self, pattern, matches, non_matches):
        for match in matches:
            self.assertTrue(fnmatch(match, pattern))
        for non_match in non_matches:
            self.assertFalse(fnmatch(non_match, pattern))

    def test_circumflex_in_set(self):
        pattern = "[^abc]"
        matches = ["^", "a", "b", "c"]
        non_matches = ["d", "e", "f", "g"]
        self._test_fnmatch(pattern, matches, non_matches)

    def test_negative_set(self):
        pattern = "[!ab]"
        matches = ["c", "d"]
        non_matches = ["a", "b"]
        self._test_fnmatch(pattern, matches, non_matches)

    def test_escaped_bracket(self):
        pattern = "[]ab]"
        matches = ["]", "a", "b"]
        non_matches = ["[]ab]", "ab]"]
        self._test_fnmatch(pattern, matches, non_matches)

    def test_empty_set(self):
        pattern = "a[]b"
        matches = ["a[]b"]
        non_matches = ["a", "b", "[", "]", "ab"]
        self._test_fnmatch(pattern, matches, non_matches)

    def test_home_dir(self):
        pattern = os.path.join("~", "a", "b")
        matches = [os.path.expanduser(os.path.join("~", "a", "b"))]
        non_matches = [os.path.join("~", "a", "b")]
        self._test_fnmatch(pattern, matches, non_matches)

    def test_alternatives(self):
        pattern = "(a|b)"
        matches = ["a", "b"]
        non_matches = ["(a|b)", "a|b"]
        self._test_fnmatch(pattern, matches, non_matches)

    def test_set_precedence(self):
        pattern = "(a|[b)]"
        matches = ["(a|b", "(a|)"]
        non_matches = ["a]", "[b]"]
        self._test_fnmatch(pattern, matches, non_matches)

    def test_questionmark(self):
        pattern = "a?b"
        matches = ["axb", "ayb"]
        non_matches = ["ab", "aXXb"]
        self._test_fnmatch(pattern, matches, non_matches)

    def test_asterisk(self):
        pattern = "a*b"
        matches = ["axb", "ayb"]
        non_matches = ["aXbX", os.path.join("a", "b")]
        self._test_fnmatch(pattern, matches, non_matches)

    def test_double_asterisk(self):
        pattern = "a**b"
        matches = ["axb", "ayb", os.path.join("a", "b")]
        non_matches = ["aXbX"]
        self._test_fnmatch(pattern, matches, non_matches)


class GlobingTest(unittest.TestCase):
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
