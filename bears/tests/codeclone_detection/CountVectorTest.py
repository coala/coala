import sys

sys.path.insert(0, ".")
import unittest
from bears.codeclone_detection.CountVector import CountVector


class CountVectorTest(unittest.TestCase):
    def test_simple_creation(self):
        uut = CountVector("varname")
        self.assertEqual(uut.count_vector, [])
        uut = CountVector("varname", [])
        self.assertEqual(uut.count_vector, [])
        self.assertRaises(AssertionError,
                          CountVector,
                          "varname",
                          [],
                          [2])

    def test_counting(self):
        uut = CountVector("varname", [lambda cursor, stack: cursor and stack])
        self.assertEqual(uut.count_vector, [0])
        uut.count_reference(True, True)
        self.assertEqual(uut.count_vector, [1])
        uut.count_reference(True, False)
        self.assertEqual(uut.count_vector, [1])

    def test_weighting(self):
        uut = CountVector("varname",
                          [lambda cursor, stack: cursor and stack,
                           lambda cursor, stack: cursor],
                          [2, 1])
        uut.count_reference(True, True)
        self.assertEqual(uut.count_vector, [2, 1])
        uut.count_reference(True, False)
        self.assertEqual(uut.count_vector, [2, 2])

    def test_conversion(self):
        uut = CountVector("varname",
                          [lambda cursor, stack: cursor and stack],
                          [2])
        uut.count_reference(True, True)
        self.assertEqual(repr(uut), str(uut))
        self.assertEqual(repr(uut), "[2]")


if __name__ == '__main__':
    unittest.main(verbosity=2)
