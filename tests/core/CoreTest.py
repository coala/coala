from concurrent.futures import ThreadPoolExecutor
import logging
import unittest
import unittest.mock

from coalib.settings.Section import Section
from coalib.core.Bear import Bear
from coalib.core.Core import initialize_dependencies, run

from coala_utils.decorators import generate_eq

from tests.core.CoreTestBase import CoreTestBase


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


class BearA(TestBearBase):
    pass


class BearB(TestBearBase):
    pass


class BearC_NeedsB(TestBearBase):
    BEAR_DEPS = {BearB}


class BearD_NeedsC(TestBearBase):
    BEAR_DEPS = {BearC_NeedsB}


class BearE_NeedsAD(TestBearBase):
    BEAR_DEPS = {BearA, BearD_NeedsC}


class FailingBear(TestBearBase):

    def analyze(self, bear, section_name, file_dict):
        raise ValueError


class BearF_NeedsFailingBear(TestBearBase):
    BEAR_DEPS = {FailingBear}


class BearG_NeedsF(TestBearBase):
    BEAR_DEPS = {BearF_NeedsFailingBear}


class BearH_NeedsG(TestBearBase):
    BEAR_DEPS = {BearG_NeedsF}


class MultiResultBear(TestBearBase):

    def analyze(self, bear, section_name, file_dict):
        yield 1
        yield 2


# This bear runs a certain number of tasks depending on the number of results
# yielded from the bears dependent on. In this case it's 3, MultiResultBear
# yields 2 results, and BearA 1.
class DynamicTaskBear(TestBearBase):
    BEAR_DEPS = {MultiResultBear, BearA}

    def analyze(self, run_id):
        return [run_id]

    def generate_tasks(self):
        tasks_count = sum(len(results)
                          for results in self.dependency_results.values())
        return (((i,), {}) for i in range(tasks_count))


class DependentOnMultipleZeroTaskBearsTestBear(TestBearBase):
    BEAR_DEPS = {type('NoTasksBear{}'.format(i),
                      (Bear,),
                      dict(generate_tasks=lambda self: tuple()))
                 for i in range(100)} | {MultiResultBear}


def get_next_instance(typ, iterable):
    """
    Reads all elements in the iterable and returns the first occurrence
    that is an instance of given type.

    :param typ:
        The type an object shall have.
    :param iterable:
        The iterable to search in.
    :return:
        The instance having ``typ`` or ``None`` if not found in
        ``iterable``.
    """
    try:
        return next(obj for obj in iterable if isinstance(obj, typ))
    except StopIteration:
        return None


class InitializeDependenciesTest(unittest.TestCase):

    def setUp(self):
        self.section1 = Section('test-section1')
        self.section2 = Section('test-section2')
        self.filedict1 = {'f1': []}
        self.filedict2 = {'f2': []}

    def test_multi_dependencies(self):
        # General test which makes use of the full dependency chain from the
        # defined classes above.
        bear_e = BearE_NeedsAD(self.section1, self.filedict1)
        dependency_tracker, bears_to_schedule = initialize_dependencies(
            {bear_e})

        self.assertEqual(len(dependency_tracker.get_dependencies(bear_e)), 2)
        self.assertTrue(any(isinstance(bear, BearA) for bear in
                            dependency_tracker.get_dependencies(bear_e)))
        self.assertTrue(any(isinstance(bear, BearD_NeedsC) for bear in
                            dependency_tracker.get_dependencies(bear_e)))

        # Test path BearE -> BearA.
        bear_a = get_next_instance(
            BearA, dependency_tracker.get_dependencies(bear_e))

        self.assertIsNotNone(bear_a)
        self.assertIs(bear_a.section, self.section1)
        self.assertIs(bear_a.file_dict, self.filedict1)
        self.assertEqual(dependency_tracker.get_dependencies(bear_a), set())

        # Test path BearE -> BearD.
        bear_d = get_next_instance(
            BearD_NeedsC, dependency_tracker.get_dependencies(bear_e))

        self.assertIsNotNone(bear_d)
        self.assertIs(bear_d.section, self.section1)
        self.assertIs(bear_d.file_dict, self.filedict1)
        self.assertEqual(len(dependency_tracker.get_dependencies(bear_d)), 1)

        # Test path BearE -> BearD -> BearC.
        self.assertEqual(len(dependency_tracker.get_dependencies(bear_d)), 1)

        bear_c = dependency_tracker.get_dependencies(bear_d).pop()

        self.assertIs(bear_c.section, self.section1)
        self.assertIs(bear_c.file_dict, self.filedict1)
        self.assertIsInstance(bear_c, BearC_NeedsB)

        # Test path BearE -> BearD -> BearC -> BearB.
        self.assertEqual(len(dependency_tracker.get_dependencies(bear_c)), 1)

        bear_b = dependency_tracker.get_dependencies(bear_c).pop()

        self.assertIs(bear_b.section, self.section1)
        self.assertIs(bear_b.file_dict, self.filedict1)
        self.assertIsInstance(bear_b, BearB)

        # No more dependencies after BearB.
        self.assertEqual(dependency_tracker.get_dependencies(bear_b), set())

        # Finally check the bears_to_schedule
        self.assertEqual(bears_to_schedule, {bear_a, bear_b})

    def test_simple(self):
        # Test simple case without dependencies.
        bear_a = BearA(self.section1, self.filedict1)
        bear_b = BearB(self.section1, self.filedict1)

        dependency_tracker, bears_to_schedule = initialize_dependencies(
            {bear_a, bear_b})

        self.assertTrue(dependency_tracker.are_dependencies_resolved)
        self.assertEqual(bears_to_schedule, {bear_a, bear_b})

    def test_reuse_instantiated_dependencies(self):
        # Test whether pre-instantiated dependency bears are correctly
        # (re)used.
        bear_b = BearB(self.section1, self.filedict1)
        bear_c = BearC_NeedsB(self.section1, self.filedict1)

        dependency_tracker, bears_to_schedule = initialize_dependencies(
            {bear_b, bear_c})

        self.assertEqual(dependency_tracker.dependants, {bear_c})
        self.assertEqual(dependency_tracker.get_dependencies(bear_c), {bear_b})

        self.assertEqual(bears_to_schedule, {bear_b})

    def test_no_reuse_of_different_section_dependency(self):
        # Test whether pre-instantiated bears which belong to different
        # sections are not (re)used, as the sections are different.
        bear_b = BearB(self.section1, self.filedict1)
        bear_c = BearC_NeedsB(self.section2, self.filedict1)

        dependency_tracker, bears_to_schedule = initialize_dependencies(
            {bear_b, bear_c})

        self.assertEqual(dependency_tracker.dependants, {bear_c})
        dependencies = dependency_tracker.dependencies
        self.assertEqual(len(dependencies), 1)
        dependency = dependencies.pop()
        self.assertIsInstance(dependency, BearB)
        self.assertIsNot(dependency, bear_b)

        self.assertEqual(bears_to_schedule, {bear_b, dependency})

    def test_different_sections_different_dependency_instances(self):
        # Test whether two bears of same type but different sections get their
        # own dependency bear instances.
        bear_c_section1 = BearC_NeedsB(self.section1, self.filedict1)
        bear_c_section2 = BearC_NeedsB(self.section2, self.filedict1)

        dependency_tracker, bears_to_schedule = initialize_dependencies(
            {bear_c_section1, bear_c_section2})

        # Test path for section1
        bear_c_s1_dependencies = dependency_tracker.get_dependencies(
            bear_c_section1)
        self.assertEqual(len(bear_c_s1_dependencies), 1)
        bear_b_section1 = bear_c_s1_dependencies.pop()
        self.assertIsInstance(bear_b_section1, BearB)

        # Test path for section2
        bear_c_s2_dependencies = dependency_tracker.get_dependencies(
            bear_c_section2)
        self.assertEqual(len(bear_c_s2_dependencies), 1)
        bear_b_section2 = bear_c_s2_dependencies.pop()
        self.assertIsInstance(bear_b_section2, BearB)

        # Test if both dependencies aren't the same.
        self.assertIsNot(bear_b_section1, bear_b_section2)

        # Test bears for schedule.
        self.assertEqual(bears_to_schedule, {bear_b_section1, bear_b_section2})

    def test_reuse_multiple_same_dependencies_correctly(self):
        # Test whether two pre-instantiated dependencies with the same section
        # and file-dictionary are correctly registered as dependencies, so only
        # a single one of those instances should be picked as a dependency.
        bear_c = BearC_NeedsB(self.section1, self.filedict1)
        bear_b1 = BearB(self.section1, self.filedict1)
        bear_b2 = BearB(self.section1, self.filedict1)

        dependency_tracker, bears_to_schedule = initialize_dependencies(
            {bear_c, bear_b1, bear_b2})

        bear_c_dependencies = dependency_tracker.get_dependencies(bear_c)
        self.assertEqual(len(bear_c_dependencies), 1)
        bear_c_dependency = bear_c_dependencies.pop()
        self.assertIsInstance(bear_c_dependency, BearB)

        self.assertIn(bear_c_dependency, {bear_b1, bear_b2})

        self.assertEqual(bears_to_schedule, {bear_b1, bear_b2})

    def test_correct_reuse_of_implicitly_instantiated_dependency(self):
        # Test if a single dependency instance is created for two different
        # instances pointing to the same section and file-dictionary.
        bear_c1 = BearC_NeedsB(self.section1, self.filedict1)
        bear_c2 = BearC_NeedsB(self.section1, self.filedict1)

        dependency_tracker, bears_to_schedule = initialize_dependencies(
            {bear_c1, bear_c2})

        # Test first path.
        bear_c1_dependencies = dependency_tracker.get_dependencies(bear_c1)
        self.assertEqual(len(bear_c1_dependencies), 1)
        bear_b1 = bear_c1_dependencies.pop()
        self.assertIsInstance(bear_b1, BearB)

        # Test second path.
        bear_c2_dependencies = dependency_tracker.get_dependencies(bear_c2)
        self.assertEqual(len(bear_c2_dependencies), 1)
        bear_b2 = bear_c2_dependencies.pop()
        self.assertIsInstance(bear_b2, BearB)

        # Test if both dependencies are actually the same.
        self.assertIs(bear_b1, bear_b2)

    def test_empty_case(self):
        # Test totally empty case.
        dependency_tracker, bears_to_schedule = initialize_dependencies(set())

        self.assertTrue(dependency_tracker.are_dependencies_resolved)
        self.assertEqual(bears_to_schedule, set())

    def test_different_filedict_different_dependency_instance(self):
        # Test whether pre-instantiated bears which have different
        # file-dictionaries assigned are not (re)used, as they have different
        # file-dictionaries.
        bear_b = BearB(self.section1, self.filedict1)
        bear_c = BearC_NeedsB(self.section1, self.filedict2)

        dependency_tracker, bears_to_schedule = initialize_dependencies(
            {bear_b, bear_c})

        self.assertEqual(dependency_tracker.dependants, {bear_c})
        dependencies = dependency_tracker.dependencies
        self.assertEqual(len(dependencies), 1)
        dependency = dependencies.pop()
        self.assertIsInstance(dependency, BearB)
        self.assertIsNot(dependency, bear_b)

        self.assertEqual(bears_to_schedule, {bear_b, dependency})

    def test_out_of_order_grouping(self):
        # Test whether the grouping supports out-of-order. Some implementations
        # (like the Python implementation of `groupby`) don't allow
        # out-of-order-grouping; if an element interrupts elements having the
        # same group, the grouping restarts. This is bad and leads to worse
        # resource allocation, as already instantiated bears could not be used
        # accordingly as dependencies, though they are eligible.

        # As `initiailize_dependencies` eliminates duplicate bears using sets,
        # it's technically impossible to test that out-of-order-grouping works
        # there perfectly. That's why we have to provoke the behaviour and make
        # a false-positive-test-succeed as improbable as possible, using a
        # huge amount of bears.
        sections = [Section('test-section' + str(i))
                    for i in range(1000)]
        bears_c = [BearC_NeedsB(section, self.filedict1)
                   for section in sections]
        bears_b = [BearB(section, self.filedict1)
                   for section in sections]

        dependency_tracker, bears_to_schedule = initialize_dependencies(
            set(bears_c) | set(bears_b))

        self.assertEqual(set(dependency_tracker), set(zip(bears_b, bears_c)))
        self.assertEqual(bears_to_schedule, set(bears_b))


class CoreTest(CoreTestBase):

    def setUp(self):
        logging.getLogger().setLevel(logging.DEBUG)

        self.section1 = Section('test-section1')
        self.filedict1 = {'f1': []}

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
        bear = MultiTaskBear(self.section1, self.filedict1, tasks_count=1)

        results = self.execute_run({bear})

        self.assertEqual(results, [0])

        self.assertEqual(bear.dependency_results, {})

    def test_run_complex(self):
        # Run a complete dependency chain.
        bear_e = BearE_NeedsAD(self.section1, self.filedict1)

        results = self.execute_run({bear_e})

        self.assertTestResultsEqual(
            results,
            [(BearA.name, self.section1.name, self.filedict1),
             (BearB.name, self.section1.name, self.filedict1),
             (BearC_NeedsB.name, self.section1.name, self.filedict1),
             (BearD_NeedsC.name, self.section1.name, self.filedict1),
             (BearE_NeedsAD.name, self.section1.name, self.filedict1)])

        # The last bear executed has to be BearE_NeedsAD.
        self.assertEqual(results[-1].bear.name, bear_e.name)

        # Check dependency results.
        # For BearE.
        self.assertIn(BearA, bear_e.dependency_results)
        self.assertIn(BearD_NeedsC, bear_e.dependency_results)
        self.assertEqual(len(bear_e.dependency_results), 2)
        self.assertTestResultsEqual(
            bear_e.dependency_results[BearA],
            [(BearA.name, self.section1.name, self.filedict1)])
        self.assertTestResultsEqual(
            bear_e.dependency_results[BearD_NeedsC],
            [(BearD_NeedsC.name, self.section1.name, self.filedict1)])

        # For BearE -> BearA.
        bear_a = get_next_instance(BearA,
                                   (result.bear for result in results))
        self.assertIsNotNone(bear_a)
        self.assertEqual(bear_a.dependency_results, {})

        # For BearE -> BearD.
        bear_d = get_next_instance(BearD_NeedsC,
                                   (result.bear for result in results))
        self.assertIsNotNone(bear_d)

        self.assertIn(BearC_NeedsB, bear_d.dependency_results)
        self.assertEqual(len(bear_d.dependency_results), 1)
        self.assertTestResultsEqual(
            bear_d.dependency_results[BearC_NeedsB],
            [(BearC_NeedsB.name, self.section1.name, self.filedict1)])

        # For BearE -> BearD -> BearC
        bear_c = get_next_instance(BearC_NeedsB,
                                   (result.bear for result in results))
        self.assertIsNotNone(bear_c)

        self.assertIn(BearB, bear_c.dependency_results)
        self.assertEqual(len(bear_c.dependency_results), 1)
        self.assertTestResultsEqual(
            bear_c.dependency_results[BearB],
            [(BearB.name, self.section1.name, self.filedict1)])

        # For BearE -> BearD -> BearC -> BearB.
        bear_b = get_next_instance(BearB,
                                   (result.bear for result in results))
        self.assertIsNotNone(bear_b)
        self.assertEqual(bear_b.dependency_results, {})

    def test_run_result_handler_exception(self):
        # Test exception in result handler. The core needs to retry to invoke
        # the handler and then exit correctly if no more results and bears are
        # left.
        bear = MultiTaskBear(self.section1, self.filedict1, tasks_count=10)

        on_result = unittest.mock.Mock(side_effect=ValueError)

        with self.assertLogs(logging.getLogger()) as cm:
            run({bear}, on_result)

        on_result.assert_has_calls([unittest.mock.call(i) for i in range(10)],
                                   any_order=True)

        self.assertEqual(len(cm.output), 10)
        for i in range(10):
            self.assertTrue(cm.output[i].startswith(
                'ERROR:root:An exception was thrown during result-handling.'))

    def test_run_bear_exception(self):
        # Test exception in bear. Core needs to shutdown directly and not wait
        # forever.
        with self.assertLogs(logging.getLogger()) as cm:
            results = self.execute_run(
                {FailingBear(self.section1, self.filedict1)})

        self.assertEqual(results, [])

        self.assertEqual(len(cm.output), 1)
        self.assertTrue(cm.output[0].startswith(
            'ERROR:root:An exception was thrown during bear execution.'))

    def test_run_bear_exception_with_other_bears(self):
        # Other bears in the core shall continue running although another one
        # crashed.
        with self.assertLogs(logging.getLogger()) as cm:
            results = self.execute_run(
                {FailingBear(self.section1, self.filedict1),
                 MultiTaskBear(self.section1, self.filedict1, tasks_count=3)})

        self.assertEqual(len(cm.output), 1)
        self.assertTrue(cm.output[0].startswith(
            'ERROR:root:An exception was thrown during bear execution.'))

        self.assertEqual(set(results), {0, 1, 2})

    def test_run_bear_with_multiple_tasks(self):
        # Test when bear is not completely finished because it has multiple
        # tasks.
        bear = MultiTaskBear(self.section1, self.filedict1, tasks_count=3)

        results = self.execute_run({bear})

        result_set = set(results)
        self.assertEqual(len(result_set), len(results))
        self.assertEqual(result_set, {0, 1, 2})
        self.assertEqual(bear.dependency_results, {})

    def test_run_bear_exception_with_dependencies(self):
        # Test when bear with dependants crashes. Dependent bears need to be
        # unscheduled and remaining non-related bears shall continue execution.
        bear_a = BearA(self.section1, self.filedict1)
        bear_failing = BearH_NeedsG(self.section1, self.filedict1)

        # bear_failing's dependency will fail, so there should only be results
        # from bear_a.
        results = self.execute_run({bear_a, bear_failing})

        self.assertTestResultsEqual(
            results,
            [(BearA.name, self.section1.name, self.filedict1)])

        self.assertEqual(bear_a.dependency_results, {})
        self.assertEqual(bear_failing.dependency_results, {})

    def test_run_bear_with_0_tasks(self):
        bear = MultiTaskBear(self.section1, self.filedict1, tasks_count=0)

        # This shall not block forever.
        results = self.execute_run({bear})

        self.assertEqual(len(results), 0)
        self.assertEqual(bear.dependency_results, {})

    def test_run_generate_tasks_dynamically_with_dependency_results(self):
        bear = DynamicTaskBear(self.section1, self.filedict1)

        results = self.execute_run({bear})

        self.assertEqual(len(results), 6)
        self.assertEqual(len(bear.dependency_results), 2)
        self.assertIn(MultiResultBear, bear.dependency_results)
        self.assertIn(BearA, bear.dependency_results)
        self.assertEqual(
            len(bear.dependency_results[MultiResultBear]), 2)
        self.assertEqual(
            len(bear.dependency_results[BearA]), 1)

    def test_run_multiple_dependency_bears_with_zero_tasks(self):
        # The core shall not stop too early because some of the bears have
        # offloaded no tasks, while others have not. This is a non-deterministic
        # issue, so we can only provoke it by offloading a huge amount of bears
        # without tasks.

        # Because bear dependencies are type-bound, we need to create many new
        # bear types doing the same so the core treats them actually as
        # different bear dependencies. Otherwise it would merge them together
        # into a single instance in the dependency-tree.
        uut = DependentOnMultipleZeroTaskBearsTestBear(self.section1,
                                                       self.filedict1)

        results = self.execute_run({uut})

        self.assertEqual(len(results), 3)
        self.assertIn(1, results)
        self.assertIn(2, results)

        uut_result = get_next_instance(TestResult, results)
        self.assertEqual(uut_result.bear.name, uut.name)
        self.assertEqual(uut_result.section_name, self.section1.name)
        self.assertEqual(uut_result.file_dict, self.filedict1)

        self.assertEqual(len(uut.dependency_results), 1)
        self.assertEqual(uut.dependency_results[MultiResultBear], [1, 2])

    def test_run_heavy_cpu_load(self):
        # No normal computer should expose 100 cores at once, so we can test
        # if the scheduler works properly.
        bear = MultiTaskBear(self.section1, self.filedict1, tasks_count=100)

        results = self.execute_run({bear})

        result_set = set(results)
        self.assertEqual(len(result_set), len(results))
        self.assertEqual(result_set, set(range(100)))
        self.assertEqual(bear.dependency_results, {})

    def test_run_empty(self):
        self.execute_run(set())


# Execute the same tests from CoreTest, but use a ThreadPoolExecutor instead.
# The core shall also seamlessly work with Python threads. Also there are
# coverage issues on Windows with ProcessPoolExecutor as coverage data isn't
# passed properly back from the pool processes.
class CoreOnThreadPoolExecutorTest(CoreTest):
    def setUp(self):
        super().setUp()
        self.executor = ThreadPoolExecutor, tuple(), dict(max_workers=8)


# This test class only runs test cases once, as the tests here rely on specific
# executors / having the control over executors.
class CoreOnSpecificExecutorTest(CoreTestBase):
    def test_custom_executor_closed_after_run(self):
        bear = MultiTaskBear(Section('test-section'),
                             {'some-file': []},
                             tasks_count=1)

        # The executor should be closed regardless how many bears are passed.
        for bears in [set(), {bear}]:
            executor = ThreadPoolExecutor(max_workers=1)

            self.execute_run(bears, executor)

            # Submitting new tasks should raise an exception now.
            with self.assertRaisesRegex(
                    RuntimeError, 'cannot schedule new futures after shutdown'):
                executor.submit(lambda: None)
