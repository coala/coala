import unittest

from coalib.misc.Iterators import pairwise


class IteratorsTest(unittest.TestCase):

    def test(self):
        test_input = [1, 2, 3, 4, "A", None]

        self.assertEqual(list(pairwise(test_input)),
                         [(1, 2), (2, 3), (3, 4), (4, "A"), ("A", None)])
