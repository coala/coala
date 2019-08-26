import unittest

from coalib.nestedlib.NlSectionPosition import NlSectionPosition
from coalib.results.TextPosition import ZeroOffsetError


class NestedPositionTest(unittest.TestCase):

    def test_initialization(self):
        with self.assertRaises(TypeError):
            NlSectionPosition(1, 'file')

        with self.assertRaises(TypeError):
            NlSectionPosition('file', 1.1)

        with self.assertRaises(TypeError):
            NlSectionPosition('file', 1, 1.1)

        with self.assertRaises(ValueError):
            NlSectionPosition('file', None, 1)

        with self.assertRaises(ZeroOffsetError):
            NlSectionPosition('file', 12, 0)

        # The following values should work
        NlSectionPosition('file', None, None)
        NlSectionPosition('file', 4, None)
        NlSectionPosition('file', 5, 4)

    def test_string_conversion(self):
        uut = NlSectionPosition('filename', 1)
        self.assertRegex(
            repr(uut),
            "<NlSectionPosition object\\(file='.*filename', line=1, "
            'column=None\\) at 0x[0-9a-fA-F]+>')
        self.assertEqual(str(uut), 'filename:1')

        uut = NlSectionPosition('None', None)
        self.assertRegex(
            repr(uut),
            "<NlSectionPosition object\\(file='.*None', line=None, "
            'column=None\\) at 0x[0-9a-fA-F]+>')
        self.assertEqual(str(uut), 'None')

        uut = NlSectionPosition('filename', 3, 2)
        self.assertEqual(str(uut), 'filename:3:2')

    # Set the setter and getter properties
    def test_properties(self):
        uut = NlSectionPosition('file', 1, 2)
        self.assertEqual(uut.line, 1)
        self.assertEqual(uut.column, 2)

        uut.line = 5
        uut.column = None
        self.assertEqual(uut.line, 5)
        self.assertEqual(uut.column, None)
