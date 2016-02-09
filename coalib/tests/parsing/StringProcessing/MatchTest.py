import unittest

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

    def test_properties2(self):
        uut = Match("alea iacta est", 48)

        self.assertEqual(uut.match, "alea iacta est")
        self.assertEqual(str(uut), "alea iacta est")
        self.assertEqual(uut.position, 48)
        self.assertEqual(uut.end_position, 62)
        self.assertEqual(uut.range, (48, 62))
        self.assertEqual(len(uut), 14)


if __name__ == '__main__':
    unittest.main(verbosity=2)
