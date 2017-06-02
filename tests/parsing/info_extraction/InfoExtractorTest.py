import os
import unittest
from contextlib import contextmanager

from coalib.parsing.info_extraction.Info import Info
from coalib.parsing.info_extraction.InfoExtractor import InfoExtractor


class InfoExtractorTest(unittest.TestCase):

    def setUp(self):
        self.current_dir = os.getcwd()

        class DummyInfo(Info):
            description = 'Some dummy information with no meaning.'

        class AnotherDummyInfo(Info):
            description = 'Another such information.'

        class DummyInfoExtractor(InfoExtractor):

            def parse_file(self, file_content):
                return file_content

            def find_information(self, fname, parsed_file):
                return [DummyInfo(
                    fname,
                    'Dummy information it is!')]

        class DummyMultiInfoExtractor(InfoExtractor):

            def parse_file(self, file_content):
                return file_content

            def find_information(self, fname, parsed_file):
                return [
                    DummyInfo(
                        fname,
                        'Dummy information it is!'),
                    DummyInfo(
                        fname,
                        'Same kind of dummy information it is!'),
                    AnotherDummyInfo(
                        fname,
                        'Another kind of dummy information!!')]

        class NoInfoExtractor(InfoExtractor):

            def parse_file(self, file_content):
                return file_content

            def find_information(self, fname, parsed_file):
                return []

        self.DummyInfo = DummyInfo
        self.DummyInfoExtractor = DummyInfoExtractor
        self.DummyMultiInfoExtractor = DummyMultiInfoExtractor
        self.NoInfoExtractor = NoInfoExtractor

    def test_implementation(self):

        uut = InfoExtractor(
            ['**'],
            self.current_dir)

        self.assertRaises(NotImplementedError, uut.parse_file, '')
        self.assertRaises(
            NotImplementedError,
            uut.find_information,
            'some_filename',
            'some_parsed_file')

    def test_multiple_target_globs(self):

        target_filenames = [
            'target_file_1',
            'target_file_2',
            'another_target_file']

        target_file_contents = ['Some content.', 'Any content', 'More content']

        uut = self.DummyInfoExtractor(
            ['target_file_**', 'another_target_file'],
            self.current_dir)

        with generate_files(
                target_filenames,
                target_file_contents,
                self.current_dir) as gen_files:

            extracted_info = uut.extract_information()

            self.assertEqual(len(extracted_info.keys()), len(target_filenames))
            self.assertEqual(extracted_info, uut.information)

            for tf in target_filenames:
                self.assertEqual(len(extracted_info[tf]['DummyInfo']), 1)
                self.assertIsInstance(
                    extracted_info[tf]['DummyInfo'][0],
                    self.DummyInfo)

    def test_multiple_information(self):

        target_filenames = ['target_file_1', ]

        target_file_contents = ['Some content.']

        uut = self.DummyMultiInfoExtractor(
            ['target_file_**', 'another_target_file'],
            self.current_dir)

        with generate_files(
                target_filenames,
                target_file_contents,
                self.current_dir) as gen_files:

            extracted_info = uut.extract_information()

            self.assertEqual(len(extracted_info.keys()), len(target_filenames))
            self.assertEqual(extracted_info, uut.information)

            for tf in target_filenames:
                self.assertEqual(len(extracted_info[tf]), 2)
                self.assertEqual(len(extracted_info[tf]['DummyInfo']), 2)
                self.assertIsInstance(
                    extracted_info[tf]['DummyInfo'][1],
                    self.DummyInfo)
                self.assertEqual(len(extracted_info[tf]['AnotherDummyInfo']), 1)
                self.assertIsInstance(
                    extracted_info[tf]['DummyInfo'][0],
                    self.DummyInfo)

    def test_no_information_found(self):
        target_filenames = ['target_file_1', ]

        target_file_contents = ['Some content.']

        uut = self.NoInfoExtractor(
            ['target_file_**', 'another_target_file'],
            self.current_dir)

        with generate_files(
                target_filenames,
                target_file_contents,
                self.current_dir) as gen_files:

            extracted_info = uut.extract_information()

            self.assertEqual(len(extracted_info.keys()), 0)
            self.assertEqual(extracted_info, uut.information)

            for tf in target_filenames:
                self.assertIsNone(extracted_info.get(tf))


@contextmanager
def generate_files(fnames, file_contents, directory=os.getcwd()):
    """
    Generates files with specified contents temporarily.

    :param fnames:        list of file names to create.
    :param file_contents: list of strings containing content
                          corresponding to the supplied file names.
    """
    fpaths = []
    try:
        for fname, fcontent in zip(fnames, file_contents):
            with open(fname, 'w', encoding='utf-8') as file:
                file.write(fcontent)
            fpaths.append(os.path.join(directory, fname))
        yield fpaths
    finally:
        for fpath in fpaths:
            os.remove(fpath)
