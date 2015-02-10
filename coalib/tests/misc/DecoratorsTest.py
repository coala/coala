import unittest
import sys

sys.path.insert(0, ".")
from coalib.misc.Decorators import unique_iterating


class CachedIteratorTestCase(unittest.TestCase):
    def test_cached_iterator(self):
        @unique_iterating
        def iterate_over_list(arg_list):
            for arg in arg_list:
                yield arg

        self.assertEqual(list(iterate_over_list([1, 1, 2, 2, 3, 3, 1, 4])),
                         [1, 2, 3, 4])


if __name__ == '__main__':
    unittest.main(verbosity=2)
