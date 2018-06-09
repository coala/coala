import unittest
from os.path import abspath

from coalib.results.SourcePosition import SourcePosition
from coalib.results.SourceRange import SourceRange
from coalib.results.AbsolutePosition import AbsolutePosition
from coalib.results.Diff import Diff


class SourceRangeTest(unittest.TestCase):

    def setUp(self):
        self.result_fileA_noline = SourcePosition('A')
        self.result_fileA_line2 = SourcePosition('A', 2)
        self.result_fileB_noline = SourcePosition('B')
        self.result_fileB_line2 = SourcePosition('B', 2)
        self.result_fileB_line4 = SourcePosition('B', 4)

    def test_construction(self):
        uut1 = SourceRange(self.result_fileA_noline)
        self.assertEqual(uut1.end, self.result_fileA_noline)

        uut2 = SourceRange.from_values('A')
        self.assertEqual(uut1, uut2)

        uut = SourceRange.from_values('B', start_line=2, end_line=4)
        self.assertEqual(uut.start, self.result_fileB_line2)
        self.assertEqual(uut.end, self.result_fileB_line4)

    def test_from_absolute_position(self):
        text = ('a\n', 'b\n')
        start = AbsolutePosition(text, 0)
        end = AbsolutePosition(text, 2)

        uut = SourceRange.from_absolute_position('F', start, end)
        compare = SourceRange.from_values('F', 1, 1, 2, 1)
        self.assertEqual(uut, compare)

        uut = SourceRange.from_absolute_position('F', start, None)
        compare = SourceRange(SourcePosition('F', 1, 1), None)
        self.assertEqual(uut, compare)

    def test_file_property(self):
        uut = SourceRange(self.result_fileA_line2)
        self.assertRegex(uut.file, '.*A')

    def test_invalid_arguments(self):
        # arguments must be SourceRanges
        with self.assertRaises(TypeError):
            SourceRange(1, self.result_fileA_noline)

        with self.assertRaises(TypeError):
            SourceRange(self.result_fileA_line2, 1)

    def test_argument_file(self):
        # both Source_Positions should describe the same file
        with self.assertRaises(ValueError):
            SourceRange(self.result_fileA_noline, self.result_fileB_noline)

    def test_argument_order(self):
        # end should come after the start
        with self.assertRaises(ValueError):
            SourceRange(self.result_fileA_line2, self.result_fileA_noline)

    def test_invalid_comparison(self):
        with self.assertRaises(TypeError):
            SourceRange(self.result_fileB_noline, self.result_fileB_line2) < 1

    def test_json(self):
        uut = SourceRange.from_values('B', start_line=2,
                                      end_line=4).__json__(use_relpath=True)
        self.assertEqual(uut['start'], self.result_fileB_line2)

    def test_contains(self):
        a = SourceRange.from_values('test_file', 1, 2, 1, 20)
        b = SourceRange.from_values('test_file', 1, 2, 1, 20)
        self.assertIn(a, b)

        a = SourceRange.from_values('test_file', 1, 2, 2, 20)
        b = SourceRange.from_values('test_file', 1, 1, 2, 20)
        self.assertIn(a, b)

        a = SourceRange.from_values('test_file', 1, 2, 1, 20)
        b = SourceRange.from_values('test_file2', 1, 2, 1, 20)
        self.assertNotIn(a, b)

        a = SourceRange.from_values('test_file', 2, 2, 64, 20)
        b = SourceRange.from_values('test_file', 1, 1, 50, 20)
        self.assertNotIn(a, b)

    def test_overlaps(self):
        a = SourceRange.from_values('test_file', 2, None, 3)
        b = SourceRange.from_values('test_file', 3, None, 5)
        self.assertTrue(a.overlaps(b))
        self.assertTrue(b.overlaps(a))

        a = SourceRange.from_values('test_file1', 2, None, 3)
        b = SourceRange.from_values('test_file2', 3, None, 5)
        self.assertFalse(a.overlaps(b))
        self.assertFalse(b.overlaps(a))

        a = SourceRange.from_values('test_file', 2, None, 2, None)
        b = SourceRange.from_values('test_file', 2, 2, 2, 80)
        self.assertTrue(a.overlaps(b))
        self.assertTrue(b.overlaps(a))

        a = SourceRange.from_values('test_file1', 1, None, None, None)
        b = SourceRange.from_values('test_file2', 1, None, 1, None)
        self.assertFalse(a.overlaps(b))
        self.assertFalse(b.overlaps(a))

        a = SourceRange.from_values('test_file', 1, None, None, None)
        b = SourceRange.from_values('test_file', 1, None, 1, None)
        self.assertTrue(a.overlaps(b))
        self.assertTrue(b.overlaps(a))

    def test_renamed_file(self):
        src_range = SourceRange(SourcePosition('test_file'))
        self.assertEqual(src_range.renamed_file({}), abspath('test_file'))

        self.assertEqual(
            src_range.renamed_file({abspath('test_file'): Diff([])}),
            abspath('test_file'))

        self.assertEqual(
            src_range.renamed_file(
                {abspath('test_file'): Diff([], rename='another_file')}),
            'another_file')


class SourceRangeExpandTest(unittest.TestCase):

    def test_expand(self):
        empty_position = SourcePosition('filename')
        file = ['abc\n', 'def\n', 'ghi\n']
        empty_range = SourceRange(empty_position, empty_position)
        full_range = SourceRange.from_values('filename', 1, 1, 3, 4)
        self.assertEqual(empty_range.expand(file), full_range)
