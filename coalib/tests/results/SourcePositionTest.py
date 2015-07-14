import sys
import unittest

sys.path.insert(0, ".")
from coalib.results.SourcePosition import SourcePosition


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
        self.assertEqual(str(uut), repr(uut))
        uut = SourcePosition(None, None)
        self.assertEqual(str(uut),
                         "file: 'None', line: None")
        self.assertEqual(str(uut), repr(uut))

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


if __name__ == '__main__':
    unittest.main(verbosity=2)
