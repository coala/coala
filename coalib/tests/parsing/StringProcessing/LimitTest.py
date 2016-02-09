import unittest

from coalib.parsing.StringProcessing.Filters import limit


class LimitTest(unittest.TestCase):
    sequence = (1, 5, 19, 22, -3, 18, 99, 500, 2015)

    def test_finite(self):
        for test_limit in (1, 2, 3, 7, 8, 10, 22, 500000):
            self.assertEqual(tuple(limit(self.sequence, test_limit)),
                             self.sequence[0:test_limit])

    def test_infinite(self):
        for test_limit in (0, -1, -2, -6555123):
            self.assertEqual(tuple(limit(self.sequence, test_limit)),
                             self.sequence)


if __name__ == '__main__':
    unittest.main(verbosity=2)
