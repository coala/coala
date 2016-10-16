import unittest

from coalib.bears.Bear import Bear
from coalib.collecting.Dependencies import (CircularDependencyError,
                                            Dependencies)
from coalib.settings.Section import Section


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

        self.dep_resolver = Dependencies()

    def test_no_deps(self):
        self.assertEqual(
            len(Dependencies.check_circular_dependency([Bear,
                                                        Bear])),
            1)

    def test_resolvable_deps(self):
        self.assertEqual(Dependencies.check_circular_dependency(
            [ResolvableBear1, ResolvableBear2]),
            [Bear, ResolvableBear1, ResolvableBear2])

    def test_unresolvable_deps(self):
        self.assertRaises(
            CircularDependencyError,
            Dependencies.check_circular_dependency,
            [UnresolvableBear1])

    def test_dependencies_resolving(self):
        self.dep_resolver.add_bear_dependencies([ResolvableBear1])
        self.assertEqual(self.dep_resolver.dependency_dict,
                         {ResolvableBear1: {Bear}})
        self.assertEqual(self.dep_resolver.dependency_set, {Bear})
        self.assertEqual(
            self.dep_resolver.resolve(Bear(Section("Name"), None)),
            [ResolvableBear1])
