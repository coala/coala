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


if __name__ == '__main__':
    unittest.main(verbosity=2)
