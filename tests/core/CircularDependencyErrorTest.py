import unittest

from coalib.core.CircularDependencyError import CircularDependencyError


class CircularDependencyErrorTest(unittest.TestCase):

    def test_default_message(self):
        with self.assertRaises(CircularDependencyError) as cm:
            raise CircularDependencyError

        self.assertEqual(str(cm.exception), 'Circular dependency detected.')

    def test_message_with_causing_node(self):
        with self.assertRaises(CircularDependencyError) as cm:
            # "3" is the causing node.
            raise CircularDependencyError(3)

        self.assertEqual(str(cm.exception),
                         'Circular dependency detected. 3 -> ... -> 3')
