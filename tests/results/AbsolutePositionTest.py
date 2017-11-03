import unittest

from coalib.results.AbsolutePosition import AbsolutePosition, calc_line_col
from coalib.misc.Constants import COMPLEX_TEST_STRING


class AbsolutePositionTest(unittest.TestCase):

    def test_calc_line_col_newlines(self):
        # no newlines
        text = ("find position of 'z'",)
        z_pos = text[0].find('z')
        self.assertEqual(
                calc_line_col(text, z_pos), (1, z_pos + 1))

        # newline
        text = ('find position of\n', "'z'",)
        string_text = ''.join(text)
        z_pos = string_text.find('z')
        self.assertEqual(calc_line_col(text, z_pos), (2, 2))

    def test_calc_line_col_unicode(self):
        uni_pos = COMPLEX_TEST_STRING.find('↑')
        self.assertEqual(
                calc_line_col((COMPLEX_TEST_STRING,), uni_pos),
                (1, uni_pos + 1))

    def test_calc_line_col_rawstrings(self):
        for raw in [(r'a\b',), (r'a\n',), ('a\\n',)]:
            pos = raw[0].find(raw[0][-1])
            self.assertEqual(calc_line_col(raw, pos), (1, 3))

    def test_calc_line_col_extremes(self):
        # End of Line
        text = ('Fitst Line\n', 'End of sencond line z')
        string_text = ''.join(text)
        z_pos = string_text.find('z')
        self.assertEqual(calc_line_col(text, z_pos),
                         (2, len(text[1])))

        # Out of text
        with self.assertRaises(ValueError):
            text = ('Some line')
            calc_line_col(text, 50)

        # start of line
        text = ('First Line\n', 'zEnd of sencond line')
        string_text = ''.join(text)
        z_pos = string_text.find('z')
        self.assertEqual(calc_line_col(text, z_pos), (2, 1))

    def test_property(self):
        uut = AbsolutePosition(('1', '2'), 1)
        self.assertEqual(uut.position, 1)
        self.assertEqual(uut.line, 2)
        self.assertEqual(uut.column, 1)

        uut = AbsolutePosition()
        self.assertEqual(uut.position, None)
        self.assertEqual(uut.line, None)
        self.assertEqual(uut.column, None)

        uut = AbsolutePosition(('a\n', 'b\n'), 0)
        self.assertEqual(uut.position, 0)
        self.assertEqual(uut.line, 1)
        self.assertEqual(uut.column, 1)

    def test_instantiation(self):
        with self.assertRaises(ValueError):
            uut = AbsolutePosition((), 0)

        uut = AbsolutePosition(position=5)
        self.assertEqual(uut.position, 5)
        self.assertEqual(uut.line, None)
        self.assertEqual(uut.column, None)
