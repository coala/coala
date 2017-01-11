import unittest

from coalib.core.ProjectBear import ProjectBear
from coalib.core.Core import run
from coalib.settings.Section import Section


class TestProjectBear(ProjectBear):

    def analyze(self, files):
        yield '\n'.join(filename + ':' + str(files[filename])
                        for filename in sorted(files))


class TestProjectBearWithParameters(ProjectBear):

    def analyze(self, files, prefix: str='!!!'):
        yield '\n'.join(prefix + filename + ':' + str(files[filename])
                        for filename in sorted(files))


class ProjectBearTest(unittest.TestCase):

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
            TestProjectBear,
            file_dict={},
            expected=[''])
        self.assertResultsEqual(
            TestProjectBear,
            file_dict={'fileX': []},
            expected=['fileX:[]'])
        self.assertResultsEqual(
            TestProjectBear,
            file_dict={'fileX': [], 'fileY': ['hello']},
            expected=["fileX:[]\nfileY:['hello']"],)
        self.assertResultsEqual(
            TestProjectBear,
            file_dict={'fileX': [], 'fileY': ['hello'], 'fileZ': ['x\ny']},
            expected=["fileX:[]\nfileY:['hello']\nfileZ:['x\\ny']"])

    def test_bear_with_parameters_but_keep_defaults(self):
        self.assertResultsEqual(
            TestProjectBearWithParameters,
            file_dict={},
            expected=[''])
        self.assertResultsEqual(
            TestProjectBearWithParameters,
            file_dict={'fileX': []},
            expected=['!!!fileX:[]'])
        self.assertResultsEqual(
            TestProjectBearWithParameters,
            file_dict={'fileX': [], 'fileY': ['hello']},
            expected=["!!!fileX:[]\n!!!fileY:['hello']"], )
        self.assertResultsEqual(
            TestProjectBearWithParameters,
            file_dict={'fileX': [], 'fileY': ['hello'], 'fileZ': ['x\ny']},
            expected=["!!!fileX:[]\n!!!fileY:['hello']\n!!!fileZ:['x\\ny']"])

    def test_bear_with_parameters(self):
        section = Section('test-section')
        section['prefix'] = '???'

        self.assertResultsEqual(
            TestProjectBearWithParameters,
            section=section,
            file_dict={},
            expected=[''])
        self.assertResultsEqual(
            TestProjectBearWithParameters,
            section=section,
            file_dict={'fileX': []},
            expected=['???fileX:[]'])
        self.assertResultsEqual(
            TestProjectBearWithParameters,
            section=section,
            file_dict={'fileX': [], 'fileY': ['hello']},
            expected=["???fileX:[]\n???fileY:['hello']"], )
        self.assertResultsEqual(
            TestProjectBearWithParameters,
            section=section,
            file_dict={'fileX': [], 'fileY': ['hello'], 'fileZ': ['x\ny']},
            expected=["???fileX:[]\n???fileY:['hello']\n???fileZ:['x\\ny']"])
