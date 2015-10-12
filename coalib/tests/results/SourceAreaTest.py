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
                         "file: 'filename', line: 1, column: None")
        self.assertRegex(
            repr(uut),
            "<SourcePosition object\\(file='filename', line=1, column=None\\) "
            "at 0x[0-9a-fA-F]+>")

        uut = SourcePosition(None, None)
        self.assertEqual(str(uut),
                         "file: None, line: None, column: None")
        self.assertRegex(
            repr(uut),
            "<SourcePosition object\\(file=None, line=None, column=None\\) at "
            "0x[0-9a-fA-F]+>")


class SourceRangeTest(unittest.TestCase):
    def test_initialization(self):
        uut = SourceRange(SourcePosition("FileA", "2"))
        self.assertEqual(uut.end, SourcePosition("FileA", "2"))

    def test_invalid_arguments(self):
        # arguments must be SourceRanges
        with self.assertRaises(TypeError):
            SourceRange(1, SourcePosition("A"))

        with self.assertRaises(TypeError):
            SourceRange(SourcePosition("A", 2), 1)

    def test_argument_file(self):
        # both Source_Positions should describe the same file
        with self.assertRaises(ValueError):
            SourceRange(SourcePosition("A"), SourcePosition("B"))

    def test_argument_order(self):
        # end should come after the start
        with self.assertRaises(ValueError):
            SourceRange(SourcePosition("A", 2), SourcePosition("A"))

    def test_invalid_comparison(self):
        with self.assertRaises(TypeError):
            SourceRange(SourcePosition("B"), SourcePosition("B", 2)) < 1
        with self.assertRaises(TypeError):
            1 < SourceRange(SourcePosition("B"), SourcePosition("B", 2))


class SourceAreaObjectComparisonTest(unittest.TestCase):
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

    def test_position_ordering(self):
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
        self.assert_ordering(SourcePosition("a file", 4, 0),
                             SourcePosition("a file", 4))
        self.assert_ordering(SourcePosition("a file", 4, 1),
                             SourcePosition("a file", 4, 2))

    def test_range_ordering(self):
        self.assert_equal(
            SourceRange(SourcePosition("B"), SourcePosition("B", 2)),
            SourceRange(SourcePosition("B"), SourcePosition("B", 2)))

        self.assertFalse(
            SourceRange(SourcePosition("B"), SourcePosition("B", 2)) ==
            SourceRange(SourcePosition("B"), SourcePosition("B", 4)))
        self.assertFalse(
            SourceRange(SourcePosition("B"), SourcePosition("B", 2)) ==
            1)

        self.assert_ordering(
            SourceRange(SourcePosition("B"), SourcePosition("B", 2)),
            SourceRange(SourcePosition("A"), SourcePosition("A", 2)))
        self.assert_ordering(
            SourceRange(SourcePosition("B", 2), SourcePosition("B", 4)),
            SourceRange(SourcePosition("B"), SourcePosition("B", 4)))
        self.assert_ordering(
            SourceRange(SourcePosition("B", 4), SourcePosition("B", 4)),
            SourceRange(SourcePosition("B", 2), SourcePosition("B", 4)))
        self.assert_ordering(
            SourceRange(SourcePosition("B"), SourcePosition("B", 4)),
            SourceRange(SourcePosition("B"), SourcePosition("B", 2)))

    def test_mutual_ordering(self):
        self.assert_ordering(
            SourceRange(SourcePosition("B", 2), SourcePosition("B", 2)),
            SourcePosition("B", 2))
        self.assert_ordering(
            SourcePosition("B", 3),
            SourceRange(SourcePosition("B", 2), SourcePosition("B", 4)))
        self.assert_ordering(
            SourceRange(SourcePosition("B", 2), SourcePosition("B", 2)),
            SourcePosition("A", 2))


if __name__ == '__main__':
    unittest.main(verbosity=2)
