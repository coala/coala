import unittest
from os.path import relpath

from coalib.results.SourcePosition import SourcePosition
from coala_utils.ContextManagers import prepare_file


class SourcePositionTest(unittest.TestCase):

    def test_initialization(self):
        with self.assertRaises(TypeError):
            SourcePosition(None, 0)

        with self.assertRaises(ValueError):
            SourcePosition('file', None, 1)

        # However these should work:
        SourcePosition('file', None, None)
        SourcePosition('file', 4, None)
        SourcePosition('file', 4, 5)

    def test_string_conversion(self):
        uut = SourcePosition('filename', 1)
        self.assertRegex(
            repr(uut),
            "<SourcePosition object\\(file='.*filename', line=1, "
            'column=None\\) at 0x[0-9a-fA-F]+>')

        uut = SourcePosition('None', None)
        self.assertRegex(
            repr(uut),
            "<SourcePosition object\\(file='.*None', line=None, column=None\\) "
            'at 0x[0-9a-fA-F]+>')

    def test_json(self):
        with prepare_file([''], None) as (_, filename):
            uut = SourcePosition(filename, 1)
            self.assertEqual(uut.__json__(use_relpath=True)
                             ['file'], relpath(filename))

    def assert_equal(self, first, second):
        self.assertGreaterEqual(first, second)
        self.assertEqual(first, second)
        self.assertLessEqual(first, second)

    def assert_ordering(self, greater, lesser):
        self.assertGreater(greater, lesser)
        self.assertGreaterEqual(greater, lesser)
        self.assertNotEqual(greater, lesser)
        self.assertLessEqual(lesser, greater)
        self.assertLess(lesser, greater)
