import sys
import unittest

sys.path.insert(0, ".")
from coalib.parsing.StringProcessing import InBetweenMatch, Match


class InBetweenMatchTest(unittest.TestCase):
    def test_properties(self):
        uut = InBetweenMatch(Match("ABC", 0), Match("DEF", 3), Match("GHI", 6))

        self.assertEqual(str(uut.begin), "ABC")
        self.assertEqual(uut.begin.position, 0)
        self.assertEqual(str(uut.inside), "DEF")
        self.assertEqual(uut.inside.position, 3)
        self.assertEqual(str(uut.end), "GHI")
        self.assertEqual(uut.end.position, 6)

        uut = InBetweenMatch.from_values("hello", 47, "world", 77, "rises", 90)

        self.assertEqual(str(uut.begin), "hello")
        self.assertEqual(uut.begin.position, 47)
        self.assertEqual(str(uut.inside), "world")
        self.assertEqual(uut.inside.position, 77)
        self.assertEqual(str(uut.end), "rises")
        self.assertEqual(uut.end.position, 90)

    def test_equal(self):
        uut = InBetweenMatch(Match("123", 4),
                             Match("456", 8),
                             Match("789", 13))

        uut2 = InBetweenMatch(Match("123", 4),
                              Match("456", 8),
                              Match("789", 13))

        self.assertNotEqual(uut, None)
        self.assertEqual(uut, uut)
        self.assertEqual(uut, uut2)
        self.assertEqual(uut2, uut)

        uut2 = InBetweenMatch(Match("123", 34089234890),
                              Match("456", 8),
                              Match("789", 13))

        self.assertNotEqual(uut, uut2)
        self.assertNotEqual(uut2, uut)

        uut2 = InBetweenMatch(Match("123", 4),
                              Match("456", 234902349034890),
                              Match("789", 13))

        self.assertNotEqual(uut, uut2)
        self.assertNotEqual(uut2, uut)

        uut2 = InBetweenMatch(Match("123", 4),
                              Match("456", 8),
                              Match("789", 1323490234890423))

        self.assertNotEqual(uut, uut2)
        self.assertNotEqual(uut2, uut)


if __name__ == '__main__':
    unittest.main(verbosity=2)
