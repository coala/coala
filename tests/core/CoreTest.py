import logging
import unittest
import unittest.mock

from coalib.settings.Section import Section
from coalib.core.Bear import Bear
from coalib.core.Core import run

from coala_utils.decorators import generate_eq


# Classes are hashed by instance, so they can be placed inside a set, compared
# to normal tuples which hash their contents. This allows to pass the file-dict
# into results.
@generate_eq('bear', 'section_name', 'file_dict')
class TestResult:

    def __init__(self, bear, section_name, file_dict):
        self.bear = bear
        self.section_name = section_name
        self.file_dict = file_dict


class TestBearBase(Bear):
    BEAR_DEPS = set()

    def analyze(self, bear, section_name, file_dict):
        # The bear can in fact return everything (so it's not bound to actual
        # `Result`s), but it must be at least an iterable.
        return [TestResult(bear, section_name, file_dict)]

    def generate_tasks(self):
        # Choose single task parallelization for simplicity. Also use the
        # section name as a parameter instead of the section itself, as compare
        # operations on tests do not succeed on them due to the pickling of
        # multiprocessing to transfer objects to the other process, which
        # instantiates a new section on each transfer.
        return ((self, self.section.name, self.file_dict), {}),


class MultiTaskBear(Bear):
    BEAR_DEPS = set()

    def __init__(self, section, file_dict, tasks_count=1):
        Bear.__init__(self, section, file_dict)
        self.tasks_count = tasks_count

    def analyze(self, run_id):
        return [run_id]

    def generate_tasks(self):
        # Choose single task parallelization for simplicity. Also use the
        # section name as a parameter instead of the section itself, as compare
        # operations on tests do not succeed on them due to the pickling of
        # multiprocessing to transfer objects to the other process, which
        # instantiates a new section on each transfer.
        return (((i,), {}) for i in range(self.tasks_count))


class FailingBear(TestBearBase):

    def analyze(self, bear, section_name, file_dict):
        raise ValueError


class CoreTest(unittest.TestCase):

    def setUp(self):
        logging.getLogger().setLevel(logging.DEBUG)

    @staticmethod
    def execute_run(bears):
        results = []

        def on_result(result):
            results.append(result)

        run(bears, on_result)

        return results

    @staticmethod
    def get_comparable_results(results):
        """
        Transforms an iterable of ``TestResult`` into something comparable.

        Some ``TestResult`` instances returned by ``run`` contain instance
        values. Due to the ``ProcessPoolExecutor``, objects get pickled,
        are transferred to the other process and are re-instantiated,
        effectively changing the id of them. The same happens again on the
        transfer back in the results, so we need something that can be
        compared.

        This function extracts relevant values into a tuple, containing::

            (test_result.bear.name,
             test_result.section_name,
             test_result.file_dict)

        :param results:
            The results to transform.
        :return:
            A list of comparable results for tests.
        """
        return [(result.bear.name, result.section_name, result.file_dict)
                for result in results]

    def assertTestResultsEqual(self, real, expected):
        """
        Test whether results from ``execute_run`` do equal with the ones given.

        This function does a sequence comparison without order, so for example
        ``[1, 2, 1]`` and ``[2, 1, 1]`` are considered equal.

        :param real:
            The actual results.
        :param expected:
            The expected results.
        """
        comparable_real = self.get_comparable_results(real)

        self.assertEqual(len(comparable_real), len(expected))
        for result in expected:
            self.assertIn(result, comparable_real)
            comparable_real.remove(result)

    def test_run_simple(self):
        # Test single bear without dependencies.
        section = Section('test-section')
        filedict = {}

        bear = MultiTaskBear(section, filedict, tasks_count=1)

        results = self.execute_run({bear})

        self.assertEqual(results, [0])

    def test_run_result_handler_exception(self):
        # Test exception in result handler. The core needs to retry to invoke
        # the handler and then exit correctly if no more results and bears are
        # left.
        bear = MultiTaskBear(
            Section('test-section'), {}, tasks_count=10)

        on_result = unittest.mock.Mock(side_effect=ValueError)

        run({bear}, on_result)

        on_result.assert_has_calls([unittest.mock.call(i) for i in range(10)],
                                   any_order=True)

    def test_run_bear_exception(self):
        # Test exception in bear. Core needs to shutdown directly and not wait
        # forever.
        self.execute_run({FailingBear(Section('test-section'), {})})

    def test_run_bear_with_multiple_tasks(self):
        # Test when bear is not completely finished because it has multiple
        # tasks.
        bear = MultiTaskBear(
            Section('test-section'), {}, tasks_count=3)

        results = self.execute_run({bear})

        result_set = set(results)
        self.assertEqual(len(result_set), len(results))
        self.assertEqual(result_set, {0, 1, 2})

    def test_run_bear_with_0_tasks(self):
        section = Section('test-section')
        filedict = {}

        bear = MultiTaskBear(section, filedict, tasks_count=0)

        # This shall not block forever.
        results = self.execute_run({bear})

        self.assertEqual(len(results), 0)

    def test_run_heavy_cpu_load(self):
        section = Section('test-section')
        filedict = {}

        # No normal computer should expose 100 cores at once, so we can test
        # if the scheduler works properly.
        bear = MultiTaskBear(section, filedict, tasks_count=100)

        results = self.execute_run({bear})

        result_set = set(results)
        self.assertEqual(len(result_set), len(results))
        self.assertEqual(result_set, {i for i in range(100)})
