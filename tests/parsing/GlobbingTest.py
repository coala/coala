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
import os
import re
import unittest

from coalib.parsing.Globbing import (
    _iter_alternatives, _iter_choices, _position_is_bracketed, fnmatch, glob,
    glob_escape)


class TestFiles:
    """
    Testfiles to check glob patterns on
    """
    glob_test_root = os.path.split(__file__)[0]
    glob_test_dir = os.path.join(glob_test_root, 'GlobTestDir')
    dir1 = os.path.join(glob_test_dir, 'SubDir1')
    file11 = os.path.join(dir1, 'File11.py')
    file12 = os.path.join(dir1, 'File12.py')
    dir2 = os.path.join(glob_test_dir, 'SubDir2')
    file_paren = os.path.join(dir2, 'File(with)parentheses.txt')
    file_brack = os.path.join(dir2, 'File[with]brackets.txt')
    file1 = os.path.join(glob_test_dir, 'File1.x')
    file2 = os.path.join(glob_test_dir, 'File2.y')
    file3 = os.path.join(glob_test_dir, 'File3.z')


class GlobbingHelperFunctionsTest(unittest.TestCase):

    def test_positions(self):
        # pattern: [bracketed values]
        pattern_positions_dict = {
            '[]': [],
            '[a]': [1],
            '[][]': [1, 2],
            '[]]]': [1],
            '[[[]': [1, 2],
            '[[[][]]]': [1, 2, 5],
            '][': [],
            '][][': [],
            '[!]': [],
            '[!c]': [1, 2],
            '[!': []
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
            '': [''],
            'a': ['a'],
            'a|b': ['a', 'b'],
            'a|b|c': ['a', 'b', 'c'],
            'a|b[|]c': ['a', 'b[|]c'],
            'a|[b|c]': ['a', '[b|c]'],
            'a[|b|c]': ['a[|b|c]'],
            '[a|b|c]': ['[a|b|c]'],
            '[a]|[b]|[c]': ['[a]', '[b]', '[c]'],
            '[[a]|[b]|[c]': ['[[a]', '[b]', '[c]']
            }
        for pattern, choices in pattern_choices_dict.items():
            self.assertEqual(list(_iter_choices(pattern)), choices)

    def test_alternatives(self):
        # pattern: [alternatives]
        pattern_alternatives_dict = {
            '': [''],
            '(ab)': ['ab'],
            'a|b': ['a|b'],
            '()': [''],
            '(|)': [''],
            '(a|b)': ['a', 'b'],
            '(a|b|c)': ['a', 'b', 'c'],
            'a(b|c)': ['ab', 'ac'],
            '(a|b)(c|d)': ['ac', 'ad', 'bc', 'bd'],
            '(a|b(c|d)': ['(a|bc', '(a|bd'],
            '(a[|]b)': ['a[|]b'],
            '[(]a|b)': ['[(]a|b)'],
            }
        for pattern, alternatives in pattern_alternatives_dict.items():
            self.assertEqual(sorted(list(_iter_alternatives(pattern))),
                             sorted(alternatives))


class GlobEscapeTest(unittest.TestCase):

    def test_glob_escape(self):
        input_strings = [
            'test',
            'test[',
            'test []',
            'test [[]',
            'test ]] str [',
            'test[][]',
            'test(',
            'test)',
            'test()',
            'test (1)']
        output_strings = [
            'test',
            'test[[]',
            'test [[][]]',
            'test [[][[][]]',
            'test []][]] str [[]',
            'test[[][]][[][]]',
            'test[(]',
            'test[)]',
            'test[(][)]',
            'test [(]1[)]']
        for unescaped_str, escaped_str in zip(input_strings, output_strings):
            self.assertEqual(glob_escape(unescaped_str), escaped_str)


class FnmatchTest(unittest.TestCase):

    def _test_fnmatch(self, pattern, matches, non_matches):
        for match in matches:
            self.assertTrue(fnmatch(match, pattern))
        for non_match in non_matches:
            self.assertFalse(fnmatch(non_match, pattern))

    def test_circumflex_in_set(self):
        pattern = '[^abc]'
        matches = ['^', 'a', 'b', 'c']
        non_matches = ['d', 'e', 'f', 'g']
        self._test_fnmatch(pattern, matches, non_matches)

    def test_negative_set(self):
        pattern = '[!ab]'
        matches = ['c', 'd']
        non_matches = ['a', 'b']
        self._test_fnmatch(pattern, matches, non_matches)

    def test_escaped_bracket(self):
        pattern = '[]ab]'
        matches = [']', 'a', 'b']
        non_matches = ['[]ab]', 'ab]']
        self._test_fnmatch(pattern, matches, non_matches)

    def test_empty_set(self):
        pattern = 'a[]b'
        matches = ['a[]b']
        non_matches = ['a', 'b', '[', ']', 'ab']
        self._test_fnmatch(pattern, matches, non_matches)

    def test_home_dir(self):
        pattern = os.path.join('~', 'a', 'b')
        matches = [os.path.expanduser(os.path.join('~', 'a', 'b'))]
        non_matches = [os.path.join('~', 'a', 'b')]
        self._test_fnmatch(pattern, matches, non_matches)

    def test_alternatives(self):
        pattern = '(a|b)'
        matches = ['a', 'b']
        non_matches = ['(a|b)', 'a|b']
        self._test_fnmatch(pattern, matches, non_matches)

    def test_set_precedence(self):
        pattern = '(a|[b)]'
        matches = ['(a|b', '(a|)']
        non_matches = ['a]', '[b]']
        self._test_fnmatch(pattern, matches, non_matches)

    def test_single_sequence(self):
        pattern = '([ab])'
        matches = ['a', 'b']
        non_matches = ['[ab]', 'ab']
        self._test_fnmatch(pattern, matches, non_matches)

    def test_questionmark(self):
        pattern = 'a?b'
        matches = ['axb', 'ayb']
        non_matches = ['ab', 'aXXb']
        self._test_fnmatch(pattern, matches, non_matches)

    def test_asterisk(self):
        pattern = 'a*b'
        matches = ['axb', 'ayb']
        non_matches = ['aXbX', os.path.join('a', 'b')]
        self._test_fnmatch(pattern, matches, non_matches)

    def test_double_asterisk(self):
        pattern = 'a**b'
        matches = ['axb', 'ayb', os.path.join('a', 'b')]
        non_matches = ['aXbX']
        self._test_fnmatch(pattern, matches, non_matches)

    def test_multiple_patterns(self):
        pattern = ['a**b', 'a**c']
        matches = ['axb', 'axc']
        non_matches = ['aXbX', 'aXcX']
        self._test_fnmatch(pattern, matches, non_matches)

        pattern = []
        matches = ['anything', 'anything_else']
        non_matches = []
        self._test_fnmatch(pattern, matches, non_matches)


class GlobTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def _test_glob(self, pattern, file_list):
        results = sorted([os.path.normcase(g) for g in glob(pattern)])
        file_list = sorted([os.path.normcase(f) for f in file_list])
        self.assertEqual([i for i in results
                          if re.search(r'(__pycache__|\.pyc)', i) is None],
                         file_list)

    def test_collect_files(self):
        pattern = os.path.join(TestFiles.glob_test_dir, 'Sub*', 'File1?.py')
        file_list = [TestFiles.file11, TestFiles.file12]
        self._test_glob(pattern, file_list)

    def test_collect_dirs(self):
        pattern = os.path.join(TestFiles.glob_test_dir, 'Sub*' + os.sep)
        file_list = [TestFiles.dir1+os.sep, TestFiles.dir2+os.sep]
        self._test_glob(pattern, file_list)

    def test_collect_specific_dir(self):
        pattern = os.path.join(TestFiles.dir1 + os.sep)
        file_list = [TestFiles.dir1+os.sep]
        self._test_glob(pattern, file_list)

    def test_collect_flat(self):
        pattern = os.path.join(TestFiles.glob_test_dir, '*')
        file_list = [TestFiles.dir1,
                     TestFiles.dir2,
                     TestFiles.file1,
                     TestFiles.file2,
                     TestFiles.file3]
        self._test_glob(pattern, file_list)

    def test_collect_all(self):
        pattern = os.path.join(TestFiles.glob_test_dir, '**', '*')
        file_list = [TestFiles.dir1,
                     TestFiles.dir2,
                     TestFiles.file1,
                     TestFiles.file2,
                     TestFiles.file3,
                     TestFiles.file11,
                     TestFiles.file12,
                     TestFiles.file_paren,
                     TestFiles.file_brack]
        self._test_glob(pattern, file_list)

    def test_collect_basename(self):
        pattern = TestFiles.glob_test_dir
        file_list = [TestFiles.glob_test_dir]
        self._test_glob(pattern, file_list)

    def test_collect_none(self):
        pattern = ''
        file_list = []
        self._test_glob(pattern, file_list)

    def test_collect_specific(self):
        pattern = os.path.join(TestFiles.file12)
        file_list = [TestFiles.file12]
        self._test_glob(pattern, file_list)

    def test_collect_parentheses(self):
        pattern = os.path.join(TestFiles.glob_test_dir,
                               'SubDir[12]',
                               'File[(]with)parentheses.txt')
        file_list = [TestFiles.file_paren]
        self._test_glob(pattern, file_list)

    def test_collect_brackets(self):
        pattern = os.path.join(TestFiles.glob_test_dir,
                               'SubDir[12]',
                               'File[[]with[]]brackets.txt')
        file_list = [TestFiles.file_brack]
        self._test_glob(pattern, file_list)

    def test_collect_or(self):
        pattern = os.path.join(TestFiles.glob_test_dir, 'File?.(x|y|z)')
        file_list = [TestFiles.file1, TestFiles.file2, TestFiles.file3]
        self._test_glob(pattern, file_list)

    def test_wildcard_dir(self):
        pattern = os.path.join(TestFiles.glob_test_dir, 'SubDir?', 'File11.py')
        file_list = [TestFiles.file11]
        self._test_glob(pattern, file_list)

    def test_collect_recursive(self):
        pattern = os.path.join(TestFiles.glob_test_dir, '**', '*')
        file_list = [TestFiles.file1,
                     TestFiles.file2,
                     TestFiles.file3,
                     TestFiles.file11,
                     TestFiles.file12,
                     TestFiles.file_paren,
                     TestFiles.file_brack,
                     TestFiles.dir1,
                     TestFiles.dir2]
        self._test_glob(pattern, file_list)

    def test_collect_recursive_part_of_basename(self):
        pattern = os.path.join(TestFiles.glob_test_dir, '**.(py|[xy])')
        file_list = [TestFiles.file11,
                     TestFiles.file12,
                     TestFiles.file1,
                     TestFiles.file2]
        self._test_glob(pattern, file_list)

    def test_collect_invalid(self):
        pattern = 'NOPE'
        file_list = []
        self._test_glob(pattern, file_list)

    def test_no_dirname_recursive(self):
        old_curdir = os.curdir
        os.curdir = TestFiles.glob_test_dir
        pattern = '**'
        file_list = [TestFiles.file1,
                     TestFiles.file2,
                     TestFiles.file3,
                     TestFiles.file11,
                     TestFiles.file12,
                     TestFiles.file_paren,
                     TestFiles.file_brack,
                     TestFiles.dir1,
                     TestFiles.dir2]
        results = sorted([os.path.normcase(os.path.join(os.curdir, g))
                          for g in glob(pattern)])
        file_list = sorted([os.path.normcase(f) for f in file_list])
        self.assertEqual([i for i in results
                          if re.search(r'(__pycache__|\.pyc)', i) is None],
                         file_list)
        os.curdir = old_curdir

    def test_no_dirname(self):
        old_curdir = os.curdir
        os.curdir = TestFiles.glob_test_dir
        pattern = '*Dir?'
        file_list = [TestFiles.dir1,
                     TestFiles.dir2]
        results = sorted([os.path.normcase(os.path.join(os.curdir, g))
                          for g in glob(pattern)])
        file_list = sorted([os.path.normcase(f) for f in file_list])
        self.assertEqual(results, file_list)
        os.curdir = old_curdir
