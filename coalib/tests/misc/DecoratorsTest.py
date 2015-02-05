import unittest
import sys

sys.path.insert(0, ".")
from coalib.misc.Decorators import unique_iterating, arguments_to_lists


class CachedIteratorTestCase(unittest.TestCase):
    def test_cached_iterator(self):
        @unique_iterating
        def iterate_over_list(arg_list):
            for arg in arg_list:
                yield arg

        self.assertEqual(list(iterate_over_list([1, 1, 2, 2, 3, 3, 1, 4])),
                         [1, 2, 3, 4])


class ArgumentsToListsTestCase(unittest.TestCase):
    def test_arguments_to_lists(self):
        @arguments_to_lists
        def return_args(*args, **kwargs):
            return args, kwargs

        self.assertEqual(
            return_args(None, True, 1, "", "AB", [1, 2], t=(3, 4), d={"a": 1}),
            (([], [True], [1], [""], ["AB"], [1, 2]), {"t": [3, 4],
                                                       "d": [{"a": 1}]
                                                       })
        )

if __name__ == '__main__':
    unittest.main(verbosity=2)
