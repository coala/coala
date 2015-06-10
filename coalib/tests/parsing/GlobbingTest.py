"""
Tests Globbing and related functions

Test Files are local and permanent and organized as follows:

GlobTestDir
├── SubDir1
│   ├── File11.py
│   └── File12.py
│ SubDir2
│   ├── File(with)parentheses.txt
│   └── File[with]brackets.txt
├── File1.x
├── File2.y
└── File3.z
"""
import inspect
import os
import platform
import sys
import unittest

sys.path.insert(0, ".")
from coalib.parsing.Globbing import _iter_alternatives
from coalib.parsing.Globbing import translate_glob_2_re
from coalib.parsing.Globbing import glob
from coalib.parsing.Globbing import fnmatch

# Testfiles to check glob patterns on
__glob_test_root__ = os.path.split(inspect.getfile(inspect.currentframe()))[0]
__glob_test_dir__ = os.path.join(__glob_test_root__, 'GlobTestDir')
__dir1__ = os.path.join(__glob_test_dir__, 'SubDir1')
__file11__ = os.path.join(__dir1__, 'File11.py')
__file12__ = os.path.join(__dir1__, 'File12.py')
__dir2__ = os.path.join(__glob_test_dir__, 'SubDir2')
__file_paren__ = os.path.join(__dir2__, 'File(with)parentheses.txt')
__file_brack__ = os.path.join(__dir2__, 'File[with]brackets.txt')
__file1__ = os.path.join(__glob_test_dir__, 'File1.x')
__file2__ = os.path.join(__glob_test_dir__, 'File2.y')
__file3__ = os.path.join(__glob_test_dir__, 'File3.z')


class IterAlternativesTest(unittest.TestCase):
    def test_basic_evaluation(self):
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

        for pattern, combinations in pattern_result_dict.items():
            results = sorted(list(_iter_alternatives(pattern)))
            self.assertEqual(results, combinations)

    def test_escaped_evaluation(self):
        pattern_result_dict = {
            "\\": ["\\"],
            "\\(\\)": ["\\(\\)"],
            "(\\|)": ["\\|"],
            "(\\||a)": ["\\|", "a"],
            "a\\bc": ["a\\bc"],
            "(\\(|\\))": ["\\(", "\\)"],
            "\\(|\\)": ["\\(", "\\)"],
            "(\\\\)": ["\\\\"],
            "\\\\(\\\\)": ["\\\\\\\\"]
            }

        for pattern, combinations in pattern_result_dict.items():
            results = sorted(list(_iter_alternatives(pattern)))
            self.assertEqual(results, combinations)

    def test_parentheses_check(self):
        pattern_list = ["(",
                        ")",
                        "())",
                        "(()",
                        "a(b|(c)d",
                        "ab|(c)d(",
                        ")(",
                        "())(",
                        "a((b|c|d)|e)(f|g))(h|i)j",
                        "(\\)",
                        "\\()",
                        "\\((\\)",
                        "()()()()(\\)()()",
                        ")\\("
                        ]

        for pattern in pattern_list:
            self.assertRaises(ValueError, list, _iter_alternatives(pattern))

    def test_long_delimiters(self):
        pattern = "AAAAAAaBBBbCCCAAAcBBBdCCCBBBeCCC"  # ((a|b)(c|d)|e)
        result_list = ["ac", "ad", "bc", "bd", "e"]
        self.assertEqual(
            sorted(list(_iter_alternatives(pattern,
                                           opening_delimiter="AAA",
                                           closing_delimiter="CCC",
                                           separator="BBB"))),
            result_list)


class TranslateGlobTest(unittest.TestCase):
    def _test_translation(self, glob, win_re, unix_re):
        if platform.system() == 'Windows':
            self.assertEqual(translate_glob_2_re(glob), win_re)
        else:
            self.assertEqual(translate_glob_2_re(glob), unix_re)

    def test_basic_glob(self):
        glob = '/home/user/projects/coala/*.py'

        correct_windows = '\\/home\\/user\\/projects\\/coala\\/(?!.*/|.*'\
            '\\\\\\\\).*\\.py\\Z(?ms)'

        correct_unix = '\\/home\\/user\\/projects\\/coala\\/[^/]*\\.py\\Z(?ms)'

        self._test_translation(glob, correct_windows, correct_unix)

    def test_complicated_glob(self):
        glob = '/h?me/**/some[thing]*/noth[!ing]/file\\|name.py'

        correct_windows = '\\/h.me\\/.*\\/some[thing](?!.*/|.*\\\\\\\\).*'\
            '\\/noth[^ing]\\/file\\|name\\.py\\Z(?ms)'

        correct_unix = '\\/h.me\\/.*\\/some[thing][^/]*\\/noth[^ing]\\/file'\
            '\\|name\\.py\\Z(?ms)'

        self._test_translation(glob, correct_windows, correct_unix)

    def test_escape_regex_stuff(self):
        glob = '(?!.*/|.*\\\\\\\\)'

        correct_windows = '\\(.\\!\\.(?!.*/|.*\\\\\\\\).*\\/\\|\\.(?!.*/|.*'\
            '\\\\\\\\).*\\\\\\\\\\)\\Z(?ms)'

        correct_unix = '\\(.\\!\\.[^/]*\\/\\|\\.[^/]*\\\\\\\\\\)\\Z(?ms)'

        self._test_translation(glob, correct_windows, correct_unix)


class GlobTest(unittest.TestCase):
    def _test_glob(self, pattern, file_list, files=True, dirs=True):
        results = sorted(glob(pattern, files, dirs))
        file_list = sorted(file_list)
        self.assertEqual(results, file_list)

    def test_collect_files(self):
        pattern = os.path.join(__glob_test_dir__, 'Sub*', 'File1?.py')
        file_list = [__file11__, __file12__]
        self._test_glob(pattern, file_list)

    def test_collect_dirs(self):
        pattern = os.path.join(__glob_test_dir__, '*')
        file_list = [__dir1__, __dir2__]
        self._test_glob(pattern, file_list, files=False)

    def test_collect_all(self):
        pattern = os.path.join(__glob_test_dir__, '**', '*')
        file_list = [__dir1__, __dir2__, __file1__, __file2__, __file3__,
                     __file11__, __file12__, __file_paren__, __file_brack__]
        self._test_glob(pattern, file_list)

    def test_collect_none(self):
        pattern = os.path.join(__glob_test_dir__, '**', '*')
        file_list = []
        self._test_glob(pattern, file_list, dirs=False, files=False)

    def test_collect_specific(self):
        pattern = os.path.join(__file1__)
        file_list = [__file1__]
        self._test_glob(pattern, file_list)

    def test_collect_escapes(self):
        pattern = os.path.join(__glob_test_dir__,
                               'SubDir[12]',
                               'File\\(with\\)parentheses.txt')
        file_list = [__file_paren__]
        self._test_glob(pattern, file_list, dirs=False)

    def test_collect_or(self):
        pattern = os.path.join(__glob_test_dir__, "File?.(x|y|z)")
        file_list = [__file1__, __file2__, __file3__]
        self._test_glob(pattern, file_list)

    def test_collect_recursive(self):
        pattern = os.path.join(__glob_test_dir__, "**", "*")
        file_list = [__file1__, __file2__, __file3__, __file11__,
                     __file12__, __file_paren__, __file_brack__]
        self._test_glob(pattern, file_list, dirs=False)


class FnmatchTest(unittest.TestCase):
    """
    fnmatch() is used extensively by glob and therefore mostly covered by
    GlobTest.
    """
    def _test_fnmatch(self, pattern, matches, non_matches):
        for match in matches:
            print("pattern {} matched by expression {}: {}! (True)".format(pattern, match, fnmatch(match, pattern)))
            self.assertTrue(fnmatch(match, pattern))
        for non_match in non_matches:
            print("pattern {} matched by expression {}: {}! (False)".format(pattern, non_match, fnmatch(non_match, pattern)))
            self.assertFalse(fnmatch(non_match, pattern))

    def test_circumflex_in_set(self):
        """
        The '^' character in a set is interesting because of it's emaning in
        regular expressions
        """
        pattern = "[^abc]"
        matches = ["^", "a", "b", "c"]
        non_matches = ["d", "e", "f", "g"]
        self._test_fnmatch(pattern, matches, non_matches)

    def test_escaped_bracket(self):
        """
        Special characters are not special in sets
        """
        pattern = "[a\\]b]"
        matches = ["ab]", "\\b]"]
        non_matches = ["a", "\\", "]", "b", "a\\]b", "[a\\]b]"]
        self._test_fnmatch(pattern, matches, non_matches)

    def test_empty_set(self):
        """
        Without a sequence inside, there is no set.
        """
        pattern = "a[]b"
        matches = ["a[]b"]
        non_matches = ["a", "b", "[", "]", "ab"]
        self._test_fnmatch(pattern, matches, non_matches)


if __name__ == '__main__':
    unittest.main(verbosity=2)
