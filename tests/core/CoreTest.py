import logging
import unittest
import unittest.mock

from coalib.settings.Section import Section
from coalib.core.Bear import Bear
from coalib.core.Core import initialize_dependencies, run

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

    def test_multi_dependencies(self):
        # General test which makes use of the full dependency chain from the
        # defined classes above.
        section = Section('test-section')
        filedict = {}

        bear_e = BearE_NeedsAD(section, filedict)
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
        self.assertIs(bear_a.section, section)
        self.assertIs(bear_a.file_dict, filedict)
        self.assertEqual(dependency_tracker.get_dependencies(bear_a), set())

        # Test path BearE -> BearD.
        bear_d = get_next_instance(
            BearD_NeedsC, dependency_tracker.get_dependencies(bear_e))

        self.assertIsNotNone(bear_d)
        self.assertIs(bear_d.section, section)
        self.assertIs(bear_a.file_dict, filedict)
        self.assertEqual(len(dependency_tracker.get_dependencies(bear_d)), 1)

        # Test path BearE -> BearD -> BearC.
        self.assertEqual(len(dependency_tracker.get_dependencies(bear_d)), 1)

        bear_c = dependency_tracker.get_dependencies(bear_d).pop()

        self.assertIs(bear_c.section, section)
        self.assertIs(bear_a.file_dict, filedict)
        self.assertIsInstance(bear_c, BearC_NeedsB)

        # Test path BearE -> BearD -> BearC -> BearB.
        self.assertEqual(len(dependency_tracker.get_dependencies(bear_c)), 1)

        bear_b = dependency_tracker.get_dependencies(bear_c).pop()

        self.assertIs(bear_b.section, section)
        self.assertIs(bear_a.file_dict, filedict)
        self.assertIsInstance(bear_b, BearB)

        # No more dependencies after BearB.
        self.assertEqual(dependency_tracker.get_dependencies(bear_b), set())

        # Finally check the bears_to_schedule
        self.assertEqual(bears_to_schedule, {bear_a, bear_b})

    def test_simple(self):
        # Test simple case without dependencies.
        section = Section('test-section')
        filedict = {}

        bear_a = BearA(section, filedict)
        bear_b = BearB(section, filedict)

        dependency_tracker, bears_to_schedule = initialize_dependencies(
            {bear_a, bear_b})

        self.assertTrue(dependency_tracker.all_dependencies_resolved)
        self.assertEqual(bears_to_schedule, {bear_a, bear_b})

    def test_reuse_instantiated_dependencies(self):
        # Test whether pre-instantiated dependency bears are correctly
        # (re)used.
        section = Section('test-section')
        filedict = {}

        bear_b = BearB(section, filedict)
        bear_c = BearC_NeedsB(section, filedict)

        dependency_tracker, bears_to_schedule = initialize_dependencies(
            {bear_b, bear_c})

        self.assertEqual(dependency_tracker.dependants, {bear_c})
        self.assertEqual(dependency_tracker.get_dependencies(bear_c), {bear_b})

        self.assertEqual(bears_to_schedule, {bear_b})

    def test_no_reuse_of_different_section_dependency(self):
        # Test whether pre-instantiated bears which belong to different
        # sections are not (re)used, as the sections are different.
        section1 = Section('test-section1')
        section2 = Section('test-section2')
        filedict = {}

        bear_b = BearB(section1, filedict)
        bear_c = BearC_NeedsB(section2, filedict)

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
        section1 = Section('test-section1')
        section2 = Section('test-section2')
        filedict = {}

        bear_c_section1 = BearC_NeedsB(section1, filedict)
        bear_c_section2 = BearC_NeedsB(section2, filedict)

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
        section = Section('test-section')
        filedict = {}

        bear_c = BearC_NeedsB(section, filedict)
        bear_b1 = BearB(section, filedict)
        bear_b2 = BearB(section, filedict)

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
        section = Section('test-section')
        filedict = {}

        bear_c1 = BearC_NeedsB(section, filedict)
        bear_c2 = BearC_NeedsB(section, filedict)

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

        self.assertTrue(dependency_tracker.all_dependencies_resolved)
        self.assertEqual(bears_to_schedule, set())

    def test_different_filedict_different_dependency_instance(self):
        # Test whether pre-instantiated bears which have different
        # file-dictionaries assigned are not (re)used, as they have different
        # file-dictionaries.
        section = Section('test-section')
        filedict1 = {'f2': []}
        filedict2 = {'f1': []}

        bear_b = BearB(section, filedict1)
        bear_c = BearC_NeedsB(section, filedict2)

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
        filedict = {}

        # As `initiailize_dependencies` eliminates duplicate bears using sets,
        # it's technically impossible to test that out-of-order-grouping works
        # there perfectly. That's why we have to provoke the behaviour and make
        # a false-positive-test-succeed as improbable as possible, using a
        # huge amount of bears.
        sections = [Section('test-section' + str(i)) for i in range(1000)]
        bears_c = [BearC_NeedsB(section, filedict) for section in sections]
        bears_b = [BearB(section, filedict) for section in sections]

        dependency_tracker, bears_to_schedule = initialize_dependencies(
            set(bears_c) | set(bears_b))

        self.assertEqual(set(dependency_tracker), set(zip(bears_b, bears_c)))
        self.assertEqual(bears_to_schedule, set(bears_b))


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
