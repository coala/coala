import sys
import unittest

sys.path.insert(0, ".")
from coalib.results.SourcePosition import SourcePosition
from coalib.results.SourceRange import SourceRange


class SourceRangeTest(unittest.TestCase):
    def setUp(self):
        self.result_fileA_noline = SourcePosition("A")
        self.result_fileA_line2 = SourcePosition("A", 2)
        self.result_fileB_noline = SourcePosition("B")
        self.result_fileB_line2 = SourcePosition("B", 2)
        self.result_fileB_line4 = SourcePosition("B", 4)

    def test_simple_construction(self):
        uut = SourceRange(self.result_fileA_noline)
        self.assertEqual(uut.end, self.result_fileA_noline)

        # If we don't give an end, end shall be start, even if we modify start
        uut.start.line = 4
        self.assertEqual(uut.start, uut.end)

    def test_invalid_arguments(self):
        # arguments must be SourceRanges
        with self.assertRaises(AssertionError):
            SourceRange(1, self.result_fileA_noline)

        with self.assertRaises(AssertionError):
            SourceRange(self.result_fileA_line2, 1)

    def test_argument_file(self):
        # both Source_Positions should describe the same file
        with self.assertRaises(AssertionError):
            SourceRange(self.result_fileA_noline, self.result_fileB_noline)

    def test_argument_order(self):
        # end should come after the start
        with self.assertRaises(AssertionError):
            SourceRange(self.result_fileA_line2, self.result_fileA_noline)

    def test_order_by_file(self):
        self.assertTrue(
            SourceRange(self.result_fileA_noline, self.result_fileA_line2) <
            SourceRange(self.result_fileB_noline, self.result_fileB_line2))

    def test_order_by_line(self):
        self.assertTrue(
            SourceRange(self.result_fileB_noline, self.result_fileB_line4) <
            SourceRange(self.result_fileB_line2, self.result_fileB_line4))

        self.assertTrue(
            SourceRange(self.result_fileB_line2, self.result_fileB_line4) <
            SourceRange(self.result_fileB_line4, self.result_fileB_line4))

    def test_order_by_end(self):
        self.assertTrue(
            SourceRange(self.result_fileB_noline, self.result_fileB_line2) <
            SourceRange(self.result_fileB_noline, self.result_fileB_line4))

    def test_equality(self):
        self.assertTrue(
            SourceRange(self.result_fileB_noline, self.result_fileB_line2) ==
            SourceRange(self.result_fileB_noline, self.result_fileB_line2))

        self.assertFalse(
            SourceRange(self.result_fileB_noline, self.result_fileB_line2) ==
            SourceRange(self.result_fileB_noline, self.result_fileB_line4))

        self.assertFalse(
            SourceRange(self.result_fileB_noline, self.result_fileB_line2) ==
            1)

    def test_invalid_comparison(self):
        with self.assertRaises(TypeError):
            SourceRange(self.result_fileB_noline, self.result_fileB_line2) < 1


if __name__ == '__main__':
    unittest.main(verbosity=2)
