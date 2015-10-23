import sys
import unittest

sys.path.insert(0, ".")
from coalib.parsing.StringProcessing import Match


class MatchTest(unittest.TestCase):
    def test_properties(self):
        uut = Match("ABC", 0)

        self.assertEqual(uut.match, "ABC")
        self.assertEqual(str(uut), "ABC")
        self.assertEqual(uut.position, 0)
        self.assertEqual(uut.end_position, 3)
        self.assertEqual(uut.range, (0, 3))
        self.assertEqual(len(uut), 3)

        uut = Match("alea iacta est", 48)

        self.assertEqual(uut.match, "alea iacta est")
        self.assertEqual(str(uut), "alea iacta est")
        self.assertEqual(uut.position, 48)
        self.assertEqual(uut.end_position, 62)
        self.assertEqual(uut.range, (48, 62))
        self.assertEqual(len(uut), 14)

    def test_equal(self):
        uut = Match("match", 34)
        uut2 = Match("match", 34)

        self.assertNotEqual(uut, None)
        self.assertEqual(uut, uut)
        self.assertEqual(uut, uut2)
        self.assertEqual(uut2, uut)

        uut2 = Match("123456", 34)

        self.assertNotEqual(uut, uut2)
        self.assertNotEqual(uut2, uut)

        uut2 = Match("match", 17)

        self.assertNotEqual(uut, uut2)
        self.assertNotEqual(uut2, uut)


if __name__ == '__main__':
    unittest.main(verbosity=2)
