import sys
import unittest

sys.path.insert(0, ".")
from coalib.results.SourcePosition import SourcePosition


class SourcePositionTest(unittest.TestCase):
    def test_initialization(self):
        with self.assertRaises(AssertionError):
            SourcePosition(None, 0)

        with self.assertRaises(AssertionError):
            SourcePosition("file", None, 1)

        # However these should work:
        SourcePosition(None, None, None)
        SourcePosition("file", None, None)
        SourcePosition("file", 4, None)
        SourcePosition("file", 4, 5)

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

    def test_equality(self):
        self.assert_equal(SourcePosition(),
                          SourcePosition(None, None, None))
        self.assert_equal(SourcePosition("some"),
                          SourcePosition("some", None, None))
        self.assert_equal(SourcePosition("some", 4),
                          SourcePosition("some", 4, None))
        self.assert_equal(SourcePosition("some", 4, 5),
                          SourcePosition("some", 4, 5))

    def test_file_ordering(self):
        self.assert_ordering(SourcePosition("a file", 4),
                             SourcePosition(None, None))
        self.assert_ordering(SourcePosition("b file", 0),
                             SourcePosition("a file", 4))

    def test_line_ordering(self):
        self.assert_ordering(SourcePosition("a file", 4),
                             SourcePosition("a file", 0))
        self.assert_ordering(SourcePosition("a file", 4),
                             SourcePosition("a file", None))

    def test_column_ordering(self):
        self.assert_ordering(SourcePosition("a file", 4, 3),
                             SourcePosition("a file", 4, 2))
        self.assert_ordering(SourcePosition("a file", 4, 3),
                             SourcePosition("a file", 4, None))


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


if __name__ == '__main__':
    unittest.main(verbosity=2)
