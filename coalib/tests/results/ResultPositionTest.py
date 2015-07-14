import sys
import unittest

sys.path.insert(0, ".")
from coalib.results.ResultPosition import ResultPosition


class ResultTest(unittest.TestCase):
    def test_string_conversion(self):
        uut = ResultPosition("filename", 1)
        self.assertEqual(str(uut),
                         "file: 'filename', line: 1")
        self.assertEqual(str(uut), repr(uut))
        uut = ResultPosition(None, None)
        self.assertEqual(str(uut),
                         "file: 'None', line: None")
        self.assertEqual(str(uut), repr(uut))

    def test_ordering(self):
        self.assert_equal(ResultPosition(None, None),
                          ResultPosition(None, None))
        self.assert_ordering(ResultPosition("a file", 4),
                             ResultPosition(None, None))
        self.assert_ordering(ResultPosition("b file", 0),
                             ResultPosition("a file", 4))
        self.assert_ordering(ResultPosition("a file", 4),
                             ResultPosition("a file", 0))

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
