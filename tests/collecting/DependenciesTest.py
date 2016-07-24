import unittest

from coalib.bears.Bear import Bear
from coalib.collecting import Dependencies


class ResolvableBear1(Bear):

    @staticmethod
    def get_dependencies():
        return [Bear]


class ResolvableBear2(Bear):

    @staticmethod
    def get_dependencies():
        return [ResolvableBear1, Bear]


class UnresolvableBear1(Bear):

    @staticmethod
    def get_dependencies():
        return [ResolvableBear1, Bear, UnresolvableBear3]


class UnresolvableBear2(Bear):

    @staticmethod
    def get_dependencies():
        return [ResolvableBear1, Bear, UnresolvableBear1]


class UnresolvableBear3(Bear):

    @staticmethod
    def get_dependencies():
        return [ResolvableBear1, Bear, UnresolvableBear2]


class DependenciesTest(unittest.TestCase):

    def test_no_deps(self):
        self.assertEqual(
            len(Dependencies.resolve([Bear,
                                      Bear])),
            1)

    def test_resolvable_deps(self):
        self.assertEqual(Dependencies.resolve([ResolvableBear1,
                                               ResolvableBear2]),
                         [Bear, ResolvableBear1, ResolvableBear2])

    def test_unresolvable_deps(self):
        self.assertRaises(
            Dependencies.CircularDependencyError,
            Dependencies.resolve,
            [UnresolvableBear1])
