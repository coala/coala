import unittest

from coalib.core.CircularDependencyError import CircularDependencyError
from coalib.core.DependencyTracker import DependencyTracker


class DependencyTrackerTest(unittest.TestCase):

    def test_check_circular_dependencies(self):
        uut = DependencyTracker()
        uut.add(0, 1)
        uut.add(1, 2)

        uut.check_circular_dependencies()

        uut.add(2, 0)

        with self.assertRaises(CircularDependencyError):
            uut.check_circular_dependencies()

    def test_get_dependants(self):
        uut = DependencyTracker()

        self.assertEqual(uut.get_dependants(0), set())

        uut.add(0, 1)
        uut.add(0, 2)
        uut.add(1, 3)

        self.assertEqual(uut.get_dependants(0), {1, 2})
        self.assertEqual(uut.get_dependants(1), {3})
        self.assertEqual(uut.get_dependants(2), set())

        uut.resolve(0)

        self.assertEqual(uut.get_dependants(0), set())
        self.assertEqual(uut.get_dependants(1), {3})

    def test_resolve(self):
        uut = DependencyTracker()
        uut.add(0, 1)
        uut.add(0, 2)
        uut.add(0, 3)
        uut.add(4, 5)
        uut.add(6, 0)

        self.assertEqual(uut.resolve(0), {1, 2, 3})

        # Dependants already resolved.
        self.assertEqual(uut.resolve(0), set())

        # Though 0 had a dependency, it was still forcefully resolved.
        self.assertEqual(uut.resolve(6), set())

        # Let's re-add a dependant for 0.
        uut.add(0, 1)
        self.assertEqual(uut.resolve(0), {1})

        # Test the case when we forcefully resolve a dependency, which is still
        # itself a dependant of another dependency together with another
        # dependant.
        uut.add(7, 8)
        uut.add(7, 9)
        uut.add(8, 10)

        self.assertEqual(uut.resolve(8), {10})

        # Test case when a dependant depends on multiple dependencies.
        uut.add(30, 20)
        uut.add(40, 20)

        self.assertEqual(uut.resolve(30), set())
        self.assertEqual(uut.resolve(40), {20})

    def test_are_dependencies_resolved(self):
        uut = DependencyTracker()

        self.assertTrue(uut.are_dependencies_resolved)

        uut.add(0, 1)

        self.assertFalse(uut.are_dependencies_resolved)

        uut.resolve(0)

        self.assertTrue(uut.are_dependencies_resolved)

        # Test case when dependencies were forcefully resolved.
        uut.add(0, 1)
        uut.add(1, 2)

        self.assertFalse(uut.are_dependencies_resolved)

        uut.resolve(1)

        self.assertTrue(uut.are_dependencies_resolved)
