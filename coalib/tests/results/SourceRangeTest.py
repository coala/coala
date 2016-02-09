import unittest
from collections import namedtuple

from coalib.results.SourcePosition import SourcePosition
from coalib.results.SourceRange import SourceRange


class SourceRangeTest(unittest.TestCase):

    def setUp(self):
        self.result_fileA_noline = SourcePosition("A")
        self.result_fileA_line2 = SourcePosition("A", 2)
        self.result_fileB_noline = SourcePosition("B")
        self.result_fileB_line2 = SourcePosition("B", 2)
        self.result_fileB_line4 = SourcePosition("B", 4)

    def test_construction(self):
        uut1 = SourceRange(self.result_fileA_noline)
        self.assertEqual(uut1.end, self.result_fileA_noline)

        uut2 = SourceRange.from_values("A")
        self.assertEqual(uut1, uut2)

        uut = SourceRange.from_values("B", start_line=2, end_line=4)
        self.assertEqual(uut.start, self.result_fileB_line2)
        self.assertEqual(uut.end, self.result_fileB_line4)

    def test_from_clang_range(self):
        # Simulating a clang SourceRange is easier than setting one up without
        # actually parsing a complete C file.
        ClangRange = namedtuple("ClangRange", "start end")
        ClangPosition = namedtuple("ClangPosition", "file line column")
        ClangFile = namedtuple("ClangFile", "name")
        file = ClangFile("t.c")
        start = ClangPosition(file, 1, 2)
        end = ClangPosition(file, 3, 4)

        uut = SourceRange.from_clang_range(ClangRange(start, end))
        compare = SourceRange.from_values("t.c", 1, 2, 3, 4)
        self.assertEqual(uut, compare)

    def test_file_property(self):
        uut = SourceRange(self.result_fileA_line2)
        self.assertRegex(uut.file, ".*A")

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


class SourceRangeExpandTest(unittest.TestCase):

    def test_expand(self):
        empty_position = SourcePosition("filename")
        file = ["abc\n", "def\n", "ghi\n"]
        empty_range = SourceRange(empty_position, empty_position)
        full_range = SourceRange.from_values("filename", 1, 1, 3, 4)
        self.assertEqual(empty_range.expand(file), full_range)


if __name__ == '__main__':
    unittest.main(verbosity=2)
