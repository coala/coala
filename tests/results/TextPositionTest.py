import unittest

from coalib.results.TextPosition import TextPosition


class TextPositionTest(unittest.TestCase):

    def test_fail_instantation(self):
        with self.assertRaises(ValueError):
            TextPosition(None, 2)

        with self.assertRaises(TypeError):
            TextPosition('hello', 3)

        with self.assertRaises(TypeError):
            TextPosition(4, 'world')

        with self.assertRaises(TypeError):
            TextPosition('double', 'string')

    def test_properties(self):
        uut = TextPosition(None, None)
        self.assertEqual(uut.line, None)
        self.assertEqual(uut.column, None)

        uut = TextPosition(7, None)
        self.assertEqual(uut.line, 7)
        self.assertEqual(uut.column, None)

        uut = TextPosition(8, 39)
        self.assertEqual(uut.line, 8)
        self.assertEqual(uut.column, 39)
