from concurrent.futures import ThreadPoolExecutor
from unittest.mock import ANY, patch

from coalib.core.FileBear import FileBear
from coalib.settings.Section import Section

from tests.core.CoreTestBase import CoreTestBase


class TestFileBear(FileBear):

    def analyze(self, filename, file):
        yield filename


class TestFileBearWithParameters(FileBear):

    def analyze(self, filename, file, results_per_file: int = 1):
        for i in range(results_per_file):
            yield filename + str(i)


class FileBearTest(CoreTestBase):

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
            expected=['fileX', 'fileY'])
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


# Execute the same tests from FileBearTest, but use a ThreadPoolExecutor
# instead. It shall also seamlessly work with Python threads. Also there are
# coverage issues on Windows with ProcessPoolExecutor as coverage data isn't
# passed properly back from the pool processes.
class FileBearOnThreadPoolExecutorTest(FileBearTest):
    def setUp(self):
        super().setUp()
        self.executor = ThreadPoolExecutor, tuple(), dict(max_workers=8)

    # Cache-tests require to be executed in the same Python process, as mocks
    # aren't multiprocessing capable. Thus put them here.

    def test_cache(self):
        section = Section('test-section')
        filedict1 = {'file.txt': []}
        filedict2 = {'file.txt': ['first-line\n'], 'file2.txt': ['xyz\n']}
        filedict3 = {'file.txt': ['first-line\n'], 'file2.txt': []}
        cache = {}

        with patch.object(TestFileBear, 'analyze',
                          autospec=True,
                          side_effect=TestFileBear.analyze) as mock:

            self.assertResultsEqual(TestFileBear,
                                    section=section,
                                    file_dict=filedict1,
                                    cache=cache,
                                    expected=list(filedict1.keys()))

            mock.assert_called_once_with(ANY, *next(iter(filedict1.items())))
            self.assertEqual(len(cache), 1)
            self.assertEqual(len(next(iter(cache.values()))), 1)

            mock.reset_mock()

            self.assertResultsEqual(TestFileBear,
                                    section=section,
                                    file_dict=filedict2,
                                    cache=cache,
                                    expected=list(filedict2.keys()))

            self.assertEqual(mock.call_count, 2)
            for filename, file in filedict2.items():
                mock.assert_any_call(ANY, filename, file)
            self.assertEqual(len(cache), 1)
            self.assertEqual(len(next(iter(cache.values()))), 3)

            mock.reset_mock()

            self.assertResultsEqual(TestFileBear,
                                    section=section,
                                    file_dict=filedict3,
                                    cache=cache,
                                    expected=list(filedict3.keys()))

            mock.assert_called_once_with(ANY, 'file2.txt', [])
            self.assertEqual(len(cache), 1)
            self.assertEqual(len(next(iter(cache.values()))), 4)
