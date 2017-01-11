import unittest

from coalib.core.FileBear import FileBear
from coalib.core.Core import run
from coalib.settings.Section import Section


class TestFileBear(FileBear):

    def analyze(self, filename, file):
        yield filename


class TestFileBearWithParameters(FileBear):

    def analyze(self, filename, file, results_per_file: int=1):
        for i in range(results_per_file):
            yield filename + str(i)


class FileBearTest(unittest.TestCase):

    def assertResultsEqual(self, bear_type, expected,
                           section=None, file_dict=None):
        """
        Asserts whether the expected results do match the output of the bear.

        Asserts for the results out-of-order.

        :param bear_type:
            The bear class to check.
        :param expected:
            A sequence of expected results.
        :param section:
            A section for the bear to use. By default uses a new section with
            name ``test-section``.
        :param file_dict:
            A file-dictionary for the bear to use. By default uses an empty
            dictionary.
        """
        if section is None:
            section = Section('test-section')
        if file_dict is None:
            file_dict = {}

        uut = bear_type(section, file_dict)

        results = []

        def on_result(result):
            results.append(result)

        run({uut}, on_result)

        self.assertEqual(sorted(expected), sorted(results))

    def test_bear_without_parameters(self):
        self.assertResultsEqual(
            TestFileBear,
            file_dict={},
            expected=[])
        self.assertResultsEqual(
            TestFileBear,
            file_dict={'fileX': []},
            expected=['fileX'])
        self.assertResultsEqual(
            TestFileBear,
            file_dict={'fileX': [], 'fileY': []},
            expected=['fileX', 'fileY'],)
        self.assertResultsEqual(
            TestFileBear,
            file_dict={'fileX': [], 'fileY': [], 'fileZ': []},
            expected=['fileX', 'fileY', 'fileZ'])

    def test_bear_with_parameters_but_keep_defaults(self):
        self.assertResultsEqual(
            TestFileBearWithParameters,
            file_dict={},
            expected=[])
        self.assertResultsEqual(
            TestFileBearWithParameters,
            file_dict={'fileX': []},
            expected=['fileX0'])
        self.assertResultsEqual(
            TestFileBearWithParameters,
            file_dict={'fileX': [], 'fileY': []},
            expected=['fileX0', 'fileY0'])
        self.assertResultsEqual(
            TestFileBearWithParameters,
            file_dict={'fileX': [], 'fileY': [], 'fileZ': []},
            expected=['fileX0', 'fileY0', 'fileZ0'])

    def test_bear_with_parameters(self):
        section = Section('test-section')
        section['results_per_file'] = '2'

        self.assertResultsEqual(
            TestFileBearWithParameters,
            section=section,
            file_dict={},
            expected=[])
        self.assertResultsEqual(
            TestFileBearWithParameters,
            section=section,
            file_dict={'fileX': []},
            expected=['fileX0', 'fileX1'])
        self.assertResultsEqual(
            TestFileBearWithParameters,
            section=section,
            file_dict={'fileX': [], 'fileY': []},
            expected=['fileX0', 'fileX1', 'fileY0', 'fileY1'])
        self.assertResultsEqual(
            TestFileBearWithParameters,
            section=section,
            file_dict={'fileX': [], 'fileY': [], 'fileZ': []},
            expected=['fileX0', 'fileX1', 'fileY0', 'fileY1', 'fileZ0',
                      'fileZ1'])
