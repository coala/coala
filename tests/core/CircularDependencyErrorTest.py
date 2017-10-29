import unittest

from coalib.core.CircularDependencyError import CircularDependencyError


class CircularDependencyErrorTest(unittest.TestCase):

    def test_default_message(self):
        with self.assertRaises(CircularDependencyError) as cm:
            # test the default case (names is None)
            raise CircularDependencyError

        self.assertEqual(str(cm.exception), 'Circular dependency detected.')

    def test_message_with_dependency_circle(self):

        with self.assertRaises(CircularDependencyError) as cm:
            raise CircularDependencyError(['A', 'B', 'C'])

        self.assertEqual(str(cm.exception),
                         'Circular dependency detected: A -> B -> C')
