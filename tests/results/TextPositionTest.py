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

    def test_comparison(self):
        uut1 = TextPosition(None, None)
        uut2 = TextPosition(None, None)
        self.assertTrue(uut1 >= uut2)
        self.assertTrue(uut1 <= uut2)
        self.assertFalse(uut1 > uut2)
        self.assertFalse(uut1 < uut2)

        uut1 = TextPosition(1, 2)
        uut2 = TextPosition(1, 3)
        uut3 = TextPosition(1, None)
        uut4 = TextPosition(1, 5)
        self.assertFalse(uut1 >= uut2)
        self.assertTrue(uut2 > uut1)
        self.assertFalse(uut3 > uut4)
        self.assertTrue(uut1 <= uut2)
        self.assertTrue(uut1 < uut2)
        self.assertFalse(uut1 > uut2)

        uut1 = TextPosition(2, None)
        uut2 = TextPosition(3, None)
        self.assertFalse(uut1 >= uut2)
        self.assertTrue(uut1 <= uut2)
        self.assertFalse(uut1 > uut2)
        self.assertTrue(uut1 < uut2)

        uut1 = TextPosition(None, None)
        uut2 = TextPosition(4, 5)
        self.assertTrue(uut1 >= uut2)
        self.assertTrue(uut1 <= uut2)
        self.assertFalse(uut1 < uut2)
        self.assertFalse(uut1 > uut2)

        uut1 = TextPosition(4, 8)
        uut2 = TextPosition(4, 8)
        self.assertTrue(uut1 >= uut2)
        self.assertTrue(uut2 <= uut1)
        self.assertFalse(uut1 > uut2)
        self.assertFalse(uut2 < uut1)

        uut1 = TextPosition(1, 2)
        uut2 = TextPosition(4, 3)
        self.assertTrue(uut1 < uut2)
        self.assertFalse(uut1 > uut2)

        uut1 = TextPosition(1, 4)
        uut2 = TextPosition(1, 4)
        uut3 = TextPosition(2, 8)
        uut4 = TextPosition(3, None)
        uut5 = TextPosition(3, None)
        self.assertTrue(uut1 == uut2)
        self.assertFalse(uut1 == uut3)
        self.assertTrue(uut4 == uut5)
        self.assertFalse(uut1 == uut4)
        self.assertTrue(uut1 != uut3)
        self.assertFalse(uut1 != uut2)
