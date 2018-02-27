from concurrent.futures import ThreadPoolExecutor
from unittest.mock import ANY, patch

from coalib.core.ProjectBear import ProjectBear
from coalib.settings.Section import Section

from tests.core.CoreTestBase import CoreTestBase


class TestProjectBear(ProjectBear):

    def analyze(self, files):
        yield '\n'.join(filename + ':' + str(files[filename])
                        for filename in sorted(files))


class TestProjectBearWithParameters(ProjectBear):

    def analyze(self, files, prefix: str='---'):
        yield '\n'.join(prefix + filename + ':' + str(files[filename])
                        for filename in sorted(files))


class ProjectBearTest(CoreTestBase):

    def assertResultsEqual(self, bear_type, expected,
                           section=None, file_dict=None, cache=None):
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
        :param cache:
            A cache the bear can use to speed up runs. If ``None``, no cache
            will be used.
        """
        if section is None:
            section = Section('test-section')
        if file_dict is None:
            file_dict = {}

        uut = bear_type(section, file_dict)

        results = self.execute_run({uut}, cache)

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
            file_dict={'fileX': [],
                       'fileY': ['hello']},
            expected=['fileX:[]\n'
                      "fileY:['hello']"])
        self.assertResultsEqual(
            TestProjectBear,
            file_dict={'fileX': [],
                       'fileY': ['hello'],
                       'fileZ': ['x\n', 'y']},
            expected=['fileX:[]\n'
                      "fileY:['hello']\n"
                      "fileZ:['x\\n', 'y']"])

    def test_bear_with_parameters_but_keep_defaults(self):
        self.assertResultsEqual(
            TestProjectBearWithParameters,
            file_dict={},
            expected=[''])
        self.assertResultsEqual(
            TestProjectBearWithParameters,
            file_dict={'fileX': []},
            expected=['---fileX:[]'])
        self.assertResultsEqual(
            TestProjectBearWithParameters,
            file_dict={'fileX': [],
                       'fileY': ['hello']},
            expected=['---fileX:[]\n'
                      "---fileY:['hello']"])
        self.assertResultsEqual(
            TestProjectBearWithParameters,
            file_dict={'fileX': [],
                       'fileY': ['hello'],
                       'fileZ': ['x\n', 'y']},
            expected=['---fileX:[]\n'
                      "---fileY:['hello']\n"
                      "---fileZ:['x\\n', 'y']"])

    def test_bear_with_parameters(self):
        section = Section('test-section')
        section['prefix'] = '___'

        self.assertResultsEqual(
            TestProjectBearWithParameters,
            section=section,
            file_dict={},
            expected=[''])
        self.assertResultsEqual(
            TestProjectBearWithParameters,
            section=section,
            file_dict={'fileX': []},
            expected=['___fileX:[]'])
        self.assertResultsEqual(
            TestProjectBearWithParameters,
            section=section,
            file_dict={'fileX': [],
                       'fileY': ['hello']},
            expected=['___fileX:[]\n'
                      "___fileY:['hello']"])
        self.assertResultsEqual(
            TestProjectBearWithParameters,
            section=section,
            file_dict={'fileX': [],
                       'fileY': ['hello'],
                       'fileZ': ['x\ny']},
            expected=['___fileX:[]\n'
                      "___fileY:['hello']\n"
                      "___fileZ:['x\\ny']"])


# Execute the same tests from ProjectBearTest, but use a ThreadPoolExecutor
# instead. It shall also seamlessly work with Python threads. Also there are
# coverage issues on Windows with ProcessPoolExecutor as coverage data isn't
# passed properly back from the pool processes.
class ProjectBearOnThreadPoolExecutorTest(ProjectBearTest):
    def setUp(self):
        super().setUp()
        self.executor = ThreadPoolExecutor, tuple(), dict(max_workers=8)

    # Cache-tests require to be executed in the same Python process, as mocks
    # aren't multiprocessing capable. Thus put them here.

    def test_cache(self):
        section = Section('test-section')
        filedict1 = {'file.txt': []}
        filedict2 = {'file.txt': ['first-line\n']}
        expected_results1 = ['file.txt:[]']
        expected_results2 = ["file.txt:['first-line\\n']"]
        cache = {}

        with patch.object(TestProjectBear, 'analyze',
                          autospec=True,
                          side_effect=TestProjectBear.analyze) as mock:

            self.assertResultsEqual(TestProjectBear,
                                    section=section,
                                    file_dict=filedict1,
                                    cache=cache,
                                    expected=expected_results1)
            mock.assert_called_once_with(ANY, filedict1)
            self.assertEqual(len(cache), 1)
            self.assertEqual(len(next(iter(cache.values()))), 1)

            mock.reset_mock()

            self.assertResultsEqual(TestProjectBear,
                                    section=section,
                                    file_dict=filedict1,
                                    cache=cache,
                                    expected=expected_results1)
            # Due to https://bugs.python.org/issue28380, assert_not_called()
            # is not available. The fix for this bug was not backported to
            # Python 3.5 or earlier, so to be compatible with 3.4.4 we have to
            # manually assert.
            self.assertFalse(mock.called)
            self.assertEqual(len(cache), 1)
            self.assertEqual(len(next(iter(cache.values()))), 1)

            self.assertResultsEqual(TestProjectBear,
                                    section=section,
                                    file_dict=filedict2,
                                    cache=cache,
                                    expected=expected_results2)

            mock.assert_called_once_with(ANY, filedict2)
            self.assertEqual(len(cache), 1)
            self.assertEqual(len(next(iter(cache.values()))), 2)
