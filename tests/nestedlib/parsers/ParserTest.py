import os
import unittest
from coalib.io.File import File


from coalib.nestedlib.parsers.Parser import Parser, get_file, create_nl_section
from coalib.nestedlib.NlSection import NlSection

TEST_FILE_DIR = os.path.join(os.path.split(__file__)[0],
                             'file_test_files')


class ParserTest(unittest.TestCase):

    def test_api(self):
        test_object = Parser()

        with self.assertRaises(NotImplementedError):
            test_object.parse('A')

    def test_get_file(self):
        file_test_dir = TEST_FILE_DIR
        self.test_file_path = os.path.join(file_test_dir, 'test1.txt')
        self.test_file = File(self.test_file_path)

        uut = get_file(self.test_file_path)
        self.assertEqual(self.test_file.lines, uut)

    def test_create_nl_section(self):
        self.nl_section = NlSection.from_values(file='A', index=1,
                                                language='python', start_line=2,
                                                end_line=4)

        uut = create_nl_section(file='A', index=1, language='python',
                                start_line=2, end_line=4)

        self.assertEqual(self.nl_section.file, uut.file)
        self.assertEqual(self.nl_section.index, uut.index)
        self.assertEqual(self.nl_section.language, uut.language)
        self.assertEqual(self.nl_section.start, uut.start)
        self.assertEqual(self.nl_section.end, uut.end)
