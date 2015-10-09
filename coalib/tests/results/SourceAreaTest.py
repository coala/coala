import sys
import unittest

sys.path.insert(0, ".")
from coalib.results.SourceArea import SourcePosition, SourceRange


class SourcePositionTest(unittest.TestCase):
    def test_initialization(self):
        with self.assertRaises(AssertionError):
            SourcePosition(None, 0)

        # However this should work:
        SourcePosition(None, None)
        SourcePosition("file", None)
        SourcePosition("file", 4)

    def test_string_conversion(self):
        uut = SourcePosition("filename", 1)
        self.assertEqual(str(uut),
                         "file: 'filename', line: 1")
        self.assertRegex(
            repr(uut),
            "<SourcePosition object\\(file='filename', line=1\\) at "
            "0x[0-9a-fA-F]+>")

        uut = SourcePosition(None, None)
        self.assertEqual(str(uut),
                         "file: None, line: None")
        self.assertRegex(
            repr(uut),
            "<SourcePosition object\\(file=None, line=None\\) at "
            "0x[0-9a-fA-F]+>")

    def test_ordering(self):
        self.assert_equal(SourcePosition(None, None),
                          SourcePosition(None, None))
        self.assert_ordering(SourcePosition("a file", 4),
                             SourcePosition(None, None))
        self.assert_ordering(SourcePosition("b file", 0),
                             SourcePosition("a file", 4))
        self.assert_ordering(SourcePosition("a file", 4),
                             SourcePosition("a file", 0))
        self.assert_ordering(SourcePosition("a file", 4),
                             SourcePosition("a file", None))

    def assert_equal(self, first, second):
        self.assertGreaterEqual(first, second)
        self.assertEqual(first, second)
        self.assertLessEqual(first, second)

    def assert_ordering(self, greater, lesser):
        self.assertGreater(greater, lesser)
        self.assertGreaterEqual(greater, lesser)
        self.assertNotEqual(greater, lesser)
        self.assertLessEqual(lesser, greater)
        self.assertLess(lesser, greater)


class SourceRangeTest(unittest.TestCase):
    def setUp(self):
        self.result_fileA_noline = SourcePosition("A")
        self.result_fileA_line2 = SourcePosition("A", 2)
        self.result_fileB_noline = SourcePosition("B")
        self.result_fileB_line2 = SourcePosition("B", 2)
        self.result_fileB_line4 = SourcePosition("B", 4)

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
