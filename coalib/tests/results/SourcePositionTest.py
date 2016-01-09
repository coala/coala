import sys
import unittest

sys.path.insert(0, ".")
from coalib.results.SourcePosition import SourcePosition


class SourcePositionTest(unittest.TestCase):

    def test_initialization(self):
        with self.assertRaises(TypeError):
            SourcePosition(None, 0)

        with self.assertRaises(ValueError):
            SourcePosition("file", None, 1)

        # However these should work:
        SourcePosition("file", None, None)
        SourcePosition("file", 4, None)
        SourcePosition("file", 4, 5)

    def test_string_conversion(self):
        uut = SourcePosition("filename", 1)
        self.assertRegex(
            repr(uut),
            "<SourcePosition object\\(file='filename', line=1, column=None\\) "
                "at 0x[0-9a-fA-F]+>")

        uut = SourcePosition("None", None)
        self.assertRegex(
            repr(uut),
            "<SourcePosition object\\(file='None', line=None, column=None\\) "
                "at 0x[0-9a-fA-F]+>")

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
