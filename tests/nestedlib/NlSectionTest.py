import unittest

from coalib.nestedlib.NlSection import NlSection
from coalib.nestedlib.NlSectionPosition import NlSectionPosition


class NlSectionTest(unittest.TestCase):

    def setUp(self):
        self.nested_fileA_noline = NlSectionPosition('A', None, None)
        self.nested_fileA_line2 = NlSectionPosition('A', 2)
        self.nested_fileA_line4 = NlSectionPosition('A', 4)

        self.nested_fileB_line4 = NlSectionPosition('B', 4)

        self.nested_sectionA_index = 1
        self.nested_sectionA_language = 'python'

    def test_construction(self):
        uut = NlSection(file='A', index=1, language='python',
                        start=self.nested_fileA_noline)
        self.assertEqual(uut.end, self.nested_fileA_noline)

        uut = NlSection.from_values(file='A', index=1, language='python',
                                    start_line=2, end_line=4)
        self.assertEqual(self.nested_sectionA_index, uut.index)
        self.assertEqual(self.nested_sectionA_language, uut.language)
        self.assertEqual(self.nested_fileA_line2, uut.start)
        self.assertEqual(self.nested_fileA_line4, uut.end)

        uut = NlSection.from_values(file='A', index=1, language='python',
                                    start_line=2, end_line=None,
                                    end_column=None)
        self.assertEqual(uut.end, self.nested_fileA_line2)

    def test_file_property(self):
        uut = NlSection(file='A', index=1, language='python',
                        start=self.nested_fileA_noline)
        self.assertRegex(uut.file, '.*A')

    def test_invalid_arguments(self):
        with self.assertRaises(TypeError):
            NlSection(file=1, index='asd', language=2.5,
                      start=self.nested_fileA_line2,
                      end=self.nested_fileA_line4)

        with self.assertRaises(TypeError):
            NlSection(file='A', index=1, language='python',
                      start=1)

        with self.assertRaises(TypeError):
            NlSection(file='A', index=1, language='python',
                      start=self.nested_fileA_line2, end=1)

    def test_argument_file(self):
        # both NlSectionPositions should describe the same file
        with self.assertRaises(ValueError):
            NlSection(file='A', index=1, language='python',
                      start=self.nested_fileA_line2,
                      end=self.nested_fileB_line4)

    def test_string_converstion(self):
        uut = NlSection.from_values(file='A', index=1, language='python',
                                    start_line=2)
        self.assertRegex(str(uut), '.*A: 1: python: L2: L2: L2: L2')

        uut = NlSection.from_values(file='A', index=1, language='python',
                                    start_line=None, end_line=None)
        self.assertRegex(str(uut), '.*A: 1: python')

        uut = NlSection.from_values(file='A', index=1, language='python',
                                    start_line=2, end_line=4)
        self.assertRegex(str(uut), '.*A: 1: python: L2: L4: L2: L4')

        uut = NlSection.from_values(file='A', index=1, language='python',
                                    start_line=2, start_column=4,
                                    end_line=4, end_column=8)
        self.assertRegex(
            str(uut), '.*A: 1: python: L2 C4: L4 C8: L2 C4: L4 C8')
