import unittest

from coalib.parsing.StringProcessing import InBetweenMatch, Match


class InBetweenMatchTest(unittest.TestCase):

    def test_invalid(self):
        self.assertRaises(ValueError,
                          InBetweenMatch,
                          Match("a", 10),
                          Match("b", -1),
                          Match("c", 12))

        self.assertRaises(ValueError,
                          InBetweenMatch.from_values,
                          "X",
                          1,
                          "QAD",
                          2,
                          "LK",
                          1)

        self.assertRaises(ValueError,
                          InBetweenMatch.from_values,
                          "1",
                          50,
                          "2",
                          22,
                          "3",
                          28)

    def test_properties(self):
        uut = InBetweenMatch(Match("ABC", 0), Match("DEF", 3), Match("GHI", 6))

        self.assertEqual(str(uut.begin), "ABC")
        self.assertEqual(uut.begin.position, 0)
        self.assertEqual(str(uut.inside), "DEF")
        self.assertEqual(uut.inside.position, 3)
        self.assertEqual(str(uut.end), "GHI")
        self.assertEqual(uut.end.position, 6)

    def test_from_values(self):
        uut = InBetweenMatch.from_values("hello", 47, "world", 77, "rises", 90)

        self.assertEqual(str(uut.begin), "hello")
        self.assertEqual(uut.begin.position, 47)
        self.assertEqual(str(uut.inside), "world")
        self.assertEqual(uut.inside.position, 77)
        self.assertEqual(str(uut.end), "rises")
        self.assertEqual(uut.end.position, 90)


if __name__ == '__main__':
    unittest.main(verbosity=2)
