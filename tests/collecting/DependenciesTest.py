import unittest

from coalib.bears.Bear import Bear
from coalib.collecting import Dependencies


class ResolvableBear1(Bear):

    BEAR_DEPS = {Bear}


class ResolvableBear2(Bear):

    BEAR_DEPS = {ResolvableBear1, Bear}


class UnresolvableBear1(Bear):

    BEAR_DEPS = {ResolvableBear1, Bear}


class UnresolvableBear2(Bear):

    BEAR_DEPS = {ResolvableBear1, Bear, UnresolvableBear1}


class UnresolvableBear3(Bear):

    BEAR_DEPS = {ResolvableBear1, Bear, UnresolvableBear2}


class DependenciesTest(unittest.TestCase):

    def setUp(self):
        # We can set this attribute properly only after UnresolvableBear3 is
        # declared.
        setattr(UnresolvableBear1, 'BEAR_DEPS', {ResolvableBear1,
                                                 Bear,
                                                 UnresolvableBear3})

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
