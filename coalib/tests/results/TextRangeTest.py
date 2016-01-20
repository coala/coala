import sys
import unittest

sys.path.insert(0, ".")
from coalib.results.TextPosition import TextPosition
from coalib.results.TextRange import TextRange


class TextRangeTest(unittest.TestCase):

    def test_fail_instantation(self):
        with self.assertRaises(ValueError):
            TextRange(TextPosition(3, 4), TextPosition(2, 8))

        with self.assertRaises(ValueError):
            TextRange(TextPosition(0, 10), TextPosition(0, 7))

        with self.assertRaises(TypeError):
            TextRange(None, TextPosition(20, 80))

        with self.assertRaises(TypeError):
            TextRange("string", TextPosition(200, 800))

        with self.assertRaises(TypeError):
            TextRange(TextPosition(5, 0), "schtring")

    def test_properties(self):
        uut = TextRange(TextPosition(7, 2), TextPosition(7, 3))
        self.assertEqual(uut.start, TextPosition(7, 2))
        self.assertEqual(uut.end, TextPosition(7, 3))

        uut = TextRange(TextPosition(70, 20), None)
        self.assertEqual(uut.start, TextPosition(70, 20))
        self.assertEqual(uut.end, TextPosition(70, 20))
        self.assertIs(uut.start, uut.end)

    def test_from_values(self):
        # Check if invalid ranges still fail.
        with self.assertRaises(ValueError):
            TextRange.from_values(0, 10, 0, 7)

        uut = TextRange.from_values(1, 0, 7, 3)
        self.assertEqual(uut.start, TextPosition(1, 0))
        self.assertEqual(uut.end, TextPosition(7, 3))

        uut = TextRange.from_values(1, 0, None, 88)
        self.assertEqual(uut.start, TextPosition(1, 0))
        self.assertEqual(uut.end, TextPosition(1, 0))

        uut = TextRange.from_values(1, 0, 7, None)
        self.assertEqual(uut.start, TextPosition(1, 0))
        self.assertEqual(uut.end, TextPosition(7, None))

        # Test defaults.
        uut = TextRange.from_values()
        self.assertEqual(uut.start, TextPosition(None, None))
        self.assertEqual(uut.end, TextPosition(None, None))

    def test_no_overlap(self):
        uut1 = TextRange.from_values(2, None, 3)
        uut2 = TextRange.from_values(4, None, 5)
        self.assertFalse(uut1.overlaps(uut2))
        self.assertFalse(uut2.overlaps(uut1))

        uut1 = TextRange.from_values(2, None, 3, 6)
        uut2 = TextRange.from_values(3, 7, 5)
        self.assertFalse(uut1.overlaps(uut2))
        self.assertFalse(uut2.overlaps(uut1))

    def test_overlap(self):
        uut1 = TextRange.from_values(2, None, 3)
        uut2 = TextRange.from_values(3, None, 5)
        self.assertTrue(uut1.overlaps(uut2))
        self.assertTrue(uut2.overlaps(uut1))

        uut1 = TextRange.from_values(2, None, 3, 6)
        uut2 = TextRange.from_values(3, 6, 5)
        self.assertTrue(uut1.overlaps(uut2))
        self.assertTrue(uut2.overlaps(uut1))

        uut1 = TextRange.from_values(2, None, 7)
        uut2 = TextRange.from_values(3, None, 5)
        self.assertTrue(uut1.overlaps(uut2))
        self.assertTrue(uut2.overlaps(uut1))

        uut1 = TextRange.from_values(5, None, 7)
        uut2 = TextRange.from_values(3, None, 6)
        self.assertTrue(uut1.overlaps(uut2))
        self.assertTrue(uut2.overlaps(uut1))


if __name__ == '__main__':
    unittest.main(verbosity=2)
