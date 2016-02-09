import unittest

from coalib.bears.Bear import Bear
from coalib.collecting import Dependencies


class BearWithoutDeps(Bear):

    @staticmethod
    def get_dependencies():
        return []


class ResolvableBear1(Bear):

    @staticmethod
    def get_dependencies():
        return [BearWithoutDeps]


class ResolvableBear2(Bear):

    @staticmethod
    def get_dependencies():
        return [ResolvableBear1, BearWithoutDeps]


class UnresolvableBear1(Bear):

    @staticmethod
    def get_dependencies():
        return [ResolvableBear1, BearWithoutDeps, UnresolvableBear3]


class UnresolvableBear2(Bear):

    @staticmethod
    def get_dependencies():
        return [ResolvableBear1, BearWithoutDeps, UnresolvableBear1]


class UnresolvableBear3(Bear):

    @staticmethod
    def get_dependencies():
        return [ResolvableBear1, BearWithoutDeps, UnresolvableBear2]


class DependenciesTest(unittest.TestCase):

    def test_no_deps(self):
        self.assertEqual(
            len(Dependencies.resolve([BearWithoutDeps,
                                      BearWithoutDeps])),
            1)

    def test_resolvable_deps(self):
        self.assertEqual(Dependencies.resolve([ResolvableBear1,
                                               ResolvableBear2]),
                         [BearWithoutDeps, ResolvableBear1, ResolvableBear2])

    def test_unresolvable_deps(self):
        self.assertRaises(
            Dependencies.CircularDependencyError,
            Dependencies.resolve,
            [UnresolvableBear1])


if __name__ == '__main__':
    unittest.main(verbosity=2)
