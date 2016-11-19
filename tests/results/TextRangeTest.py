import unittest

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
            TextRange('string', TextPosition(200, 800))

        with self.assertRaises(TypeError):
            TextRange(TextPosition(5, 0), 'schtring')

    def test_properties(self):
        uut = TextRange(TextPosition(7, 2), TextPosition(7, 3))
        self.assertEqual(uut.start, TextPosition(7, 2))
        self.assertEqual(uut.end, TextPosition(7, 3))

        uut = TextRange(TextPosition(70, 20), None)
        self.assertEqual(uut.start, TextPosition(70, 20))
        self.assertEqual(uut.end, TextPosition(70, 20))
        self.assertEqual(uut.start, uut.end)
        self.assertIsNot(uut.start, uut.end)

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

    def test_contains(self):
        range_a = TextRange.from_values(1, 1, 1, 19)
        range_b = TextRange.from_values(1, 1, 1, 20)

        self.assertIn(range_a, range_b)

        range_a = TextRange.from_values(1, 1, 1, 21)
        range_b = TextRange.from_values(1, 1, 1, 20)

        self.assertNotIn(range_a, range_b)

        range_a = TextRange.from_values(1, 5, 1, 5)
        range_b = TextRange.from_values(1, 1, 1, 20)

        self.assertIn(range_a, range_b)

        range_a = TextRange.from_values(1, 1, 1, 18)
        range_b = TextRange.from_values(1, 14, 1, 20)

        self.assertNotIn(range_a, range_b)

        range_a = TextRange.from_values(1, 1, 1, 20)
        range_b = TextRange.from_values(1, 1, 1, 20)

        self.assertIn(range_a, range_b)


class TextRangeJoinTest(unittest.TestCase):

    def setUp(self):
        self.pos = [TextPosition(1, 1),
                    TextPosition(3, 1),
                    TextPosition(3, 3),
                    TextPosition(4, 3),
                    TextPosition(5, 3)]

    def test_fails(self):
        # need to pass ranges
        with self.assertRaises(TypeError):
            TextRange.join(self.pos[0], self.pos[1])

        with self.assertRaises(TypeError):
            TextRange.join(TextRange(self.pos[0], self.pos[1]), self.pos[1])

        # ranges must overlap
        with self.assertRaises(ValueError):
            TextRange.join(TextRange(self.pos[0], self.pos[1]),
                           TextRange(self.pos[3], self.pos[4]))

    def test_join(self):
        # overlap
        self.assertEqual(TextRange.join(TextRange(self.pos[0], self.pos[2]),
                                        TextRange(self.pos[1], self.pos[3])),
                         TextRange(self.pos[0], self.pos[3]))

        self.assertEqual(TextRange.join(TextRange(self.pos[1], self.pos[3]),
                                        TextRange(self.pos[2], self.pos[4])),
                         TextRange(self.pos[1], self.pos[4]))
        # embrace
        self.assertEqual(TextRange.join(TextRange(self.pos[0], self.pos[3]),
                                        TextRange(self.pos[1], self.pos[2])),
                         TextRange(self.pos[0], self.pos[3]))

        # touch
        self.assertEqual(TextRange.join(TextRange(self.pos[1], self.pos[2]),
                                        TextRange(self.pos[2], self.pos[3])),
                         TextRange(self.pos[1], self.pos[3]))


class TextRangeExpandTest(unittest.TestCase):

    def test_expand_full(self):
        empty_position = TextPosition()
        file = ['abc\n', 'def\n', 'ghi\n']
        empty_range = TextRange(empty_position, empty_position)
        full_range = TextRange.from_values(1, 1, 3, 4)
        self.assertEqual(empty_range.expand(file), full_range)

    def test_expand_none(self):
        start_position = TextPosition(2, 2)
        end_position = TextPosition(3, 2)
        file = ['abc\n', 'def\n', 'ghi\n']
        text_range = TextRange(start_position, end_position)
        self.assertEqual(text_range.expand(file), text_range)

    def test_expand_semi(self):
        file = ['abc\n', 'defg\n', 'hijkl\n', 'mnopqr\n']
        semi_range = TextRange.from_values(2, None, 3, None)
        full_range = TextRange.from_values(2, 1, 3, 6)
        self.assertEqual(semi_range.expand(file), full_range)
