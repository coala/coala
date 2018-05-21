import os
import unittest

from coalib.io.FileFactory import FileFactory


def get_path_components(filepath):
    """
    Splits the filepath into components to provide a unique
    test results that passes on all CIs.
    """
    return os.path.normpath(filepath).split(os.sep)


class FileFactoryTest(unittest.TestCase):

    def setUp(self):
        file_factory_test_dir = os.path.join(os.path.split(__file__)[0],
                                             'FileFactoryTestFiles')

        self.test_file = os.path.join(file_factory_test_dir, 'test1.txt')
        self.other_test_file = os.path.join(file_factory_test_dir, 'test2.txt')
        self.uut = FileFactory(self.test_file)
        self.other_file_factory = FileFactory(self.other_test_file)

    def test_equal(self):
        self.assertEqual(self.uut, FileFactory(self.test_file))
        self.assertNotEqual(self.uut, self.other_file_factory)

    def test_iter(self):
        self.assertEqual(list(self.uut), ['This is a test file.'])

    def test_line(self):
        self.assertEqual(self.uut.get_line(0), 'This is a test file.')
        with self.assertRaises(IndexError):
            self.uut.get_line(1)

    def test_lines(self):
        self.assertEqual(self.uut.lines, ('This is a test file.',))

    def test_raw(self):
        self.assertEqual(self.uut.raw, b'This is a test file.')

    def test_string(self):
        self.assertEqual(self.uut.string, 'This is a test file.')

    def test_timestamp(self):
        self.assertEqual(self.uut.timestamp, os.path.getmtime(self.test_file))

    def test_name(self):
        self.assertEqual(get_path_components(self.uut.name)[-4:],
                         ['tests', 'io', 'FileFactoryTestFiles', 'test1.txt'])
