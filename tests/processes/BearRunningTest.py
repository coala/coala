import multiprocessing
import queue
import unittest

from coalib.bears.GlobalBear import GlobalBear
from coalib.bears.LocalBear import LocalBear
from coalib.processes.BearRunning import (
    LOG_LEVEL, run, send_msg, task_done)
from coalib.processes.CONTROL_ELEMENT import CONTROL_ELEMENT
from coalib.results.Result import RESULT_SEVERITY, Result
from coalib.settings.Section import Section
from testfixtures import LogCapture, StringComparison


class LocalTestBear(LocalBear):

    def run(self, filename, file):
        if filename == 'file1':
            raise Exception('Just to throw anything here.')
        return [Result.from_values('LocalTestBear',
                                   'something went wrong',
                                   filename)]


class SimpleBear(LocalBear):

    def run(self,
            filename,
            file,
            *args,
            dependency_results=None,
            **kwargs):
        return [Result.from_values('SimpleBear',
                                   'something went wrong',
                                   filename),
                # This result should not be passed to DependentBear
                Result.from_values('FakeBear',
                                   'something went wrong',
                                   filename),
                Result.from_values('SimpleBear',
                                   'another thing went wrong',
                                   filename)]


class DependentBear(LocalBear):

    BEAR_DEPS = {SimpleBear}

    def run(self,
            filename,
            file,
            *args,
            dependency_results=None,
            **kwargs):
        assert len(dependency_results['SimpleBear']) == 2


class SimpleGlobalBear(GlobalBear):

    def run(self,
            *args,
            dependency_results=None,
            **kwargs):
        return [Result('SimpleGlobalBear', 'something went wrong'),
                # This result should not be passed to DependentBear
                Result('FakeBear', 'something went wrong'),
                Result('SimpleGlobalBear', 'another thing went wrong')]


class DependentGlobalBear(GlobalBear):

    BEAR_DEPS = {SimpleGlobalBear}

    def run(self,
            *args,
            dependency_results=None,
            **kwargs):
        assert len(dependency_results['SimpleGlobalBear']) == 3


class GlobalTestBear(GlobalBear):

    def run(self):
        result = []
        for file, contents in self.file_dict.items():
            result.append(Result.from_values('GlobalTestBear',
                                             'Files are bad in general!',
                                             file,
                                             severity=RESULT_SEVERITY.INFO))
        return result


class EvilBear(LocalBear):

    def execute(self, *args, **kwargs):
        raise NotImplementedError


class UnexpectedBear1(LocalBear):

    def run(self, filename, file):
        return [1,
                Result('UnexpectedBear1', 'test result')]


class UnexpectedBear2(LocalBear):

    def run(self, filename, file):
        return 1


class BearRunningUnitTest(unittest.TestCase):

    def setUp(self):
        self.settings = Section('name')

        self.file_name_queue = queue.Queue()
        self.local_bear_list = []
        self.global_bear_list = []
        self.global_bear_queue = queue.Queue()
        self.file_dict = {}
        manager = multiprocessing.Manager()
        self.local_result_dict = manager.dict()
        self.global_result_dict = manager.dict()
        self.message_queue = queue.Queue()
        self.control_queue = queue.Queue()

    def test_queue_done_marking(self):
        self.message_queue.put('test')
        task_done(self.message_queue)  # Should make the queue joinable
        self.message_queue.join()

        task_done('test')  # Should pass silently

    def test_messaging(self):
        with LogCapture() as capture:
            send_msg(None,
                     None,
                     LOG_LEVEL.DEBUG,
                     'test',
                     'messag',
                     delimiter='-',
                     end='e')

        capture.check(
            ('root', 'DEBUG', 'test-message'),
        )

    def test_dependencies(self):
        self.local_bear_list.append(SimpleBear(self.settings,
                                               self.message_queue))
        self.local_bear_list.append(DependentBear(self.settings,
                                                  self.message_queue))
        self.global_bear_list.append(SimpleGlobalBear({},
                                                      self.settings,
                                                      self.message_queue))
        self.global_bear_list.append(DependentGlobalBear({},
                                                         self.settings,
                                                         self.message_queue))
        self.global_bear_queue.put(1)
        self.global_bear_queue.put(0)
        self.file_name_queue.put('t')
        self.file_dict['t'] = []

        run(self.file_name_queue,
            self.local_bear_list,
            self.global_bear_list,
            self.global_bear_queue,
            self.file_dict,
            self.local_result_dict,
            self.global_result_dict,
            None,
            self.control_queue)

    def test_evil_bear(self):
        self.local_bear_list.append(EvilBear(self.settings,
                                             self.message_queue))
        self.file_name_queue.put('t')
        self.file_dict['t'] = []

        run(self.file_name_queue,
            self.local_bear_list,
            self.global_bear_list,
            self.global_bear_queue,
            self.file_dict,
            self.local_result_dict,
            self.global_result_dict,
            None,
            self.control_queue)

    def test_strange_bear(self):
        self.local_bear_list.append(UnexpectedBear1(self.settings,
                                                    self.message_queue))
        self.local_bear_list.append(UnexpectedBear2(self.settings,
                                                    self.message_queue))
        self.file_name_queue.put('t')
        self.file_dict['t'] = []

        with LogCapture() as capture:
            run(self.file_name_queue,
                self.local_bear_list,
                self.global_bear_list,
                self.global_bear_queue,
                self.file_dict,
                self.local_result_dict,
                self.global_result_dict,
                None,
                self.control_queue)

        capture.check(
            ('root', 'DEBUG', 'Running bear UnexpectedBear1...'),
            ('root', 'ERROR', 'The results from the bear UnexpectedBear1 '
                              'could only be partially processed with '
                              "arguments ('t', []), {}"),
            ('root', 'DEBUG', 'One of the results in the list for the bear '
                              'UnexpectedBear1 is an instance of <class '
                              "'int'> but it should be an instance of Result"),
            ('root', 'DEBUG', 'Running bear UnexpectedBear2...'),
            ('root', 'ERROR', 'Bear UnexpectedBear2 failed to run on file '
                              't. Take a look at debug messages (`-V`) for '
                              'further information.'),
            ('root', 'DEBUG', StringComparison(r'.*The bear UnexpectedBear2 '
                                               'raised an exception*'))
        )


class BearRunningIntegrationTest(unittest.TestCase):
    example_file = """a
b
c
d
"""

    def setUp(self):
        self.settings = Section('name')

        self.file_name_queue = queue.Queue()
        self.local_bear_list = []
        self.global_bear_list = []
        self.global_bear_queue = queue.Queue()
        self.file_dict = {}
        manager = multiprocessing.Manager()
        self.local_result_dict = manager.dict()
        self.global_result_dict = manager.dict()
        self.message_queue = queue.Queue()
        self.control_queue = queue.Queue()

        self.file1 = 'file1'
        self.file2 = 'arbitrary'

        self.file_name_queue.put(self.file1)
        self.file_name_queue.put(self.file2)
        self.file_name_queue.put('invalid file')
        self.local_bear_list.append(LocalTestBear(self.settings,
                                                  self.message_queue))
        self.local_bear_list.append('not a valid bear')
        self.file_dict[self.file1] = self.example_file
        self.file_dict[self.file2] = self.example_file
        self.global_bear_list.append(GlobalTestBear(self.file_dict,
                                                    self.settings,
                                                    self.message_queue))
        self.global_bear_list.append('not a valid bear')
        self.global_bear_queue.put(0)
        self.global_bear_queue.put(1)

    def test_run(self):
        with LogCapture() as capture:
            run(self.file_name_queue,
                self.local_bear_list,
                self.global_bear_list,
                self.global_bear_queue,
                self.file_dict,
                self.local_result_dict,
                self.global_result_dict,
                None,
                self.control_queue)

        capture.check(
            ('root', 'DEBUG', 'Running bear LocalTestBear...'),
            ('root', 'ERROR', 'Bear LocalTestBear failed to run on file '
                              'file1. Take a look at debug messages (`-V`) '
                              'for further information.'),
            ('root', 'DEBUG', StringComparison(r'.*The bear LocalTestBear '
                                               'raised an exception*')),
            ('root', 'WARNING', 'A given local bear (str) is not valid. '
                                'Leaving it out... This is a bug. We are '
                                'sorry for the inconvenience. Please contact '
                                'the developers for assistance.'),
            ('root', 'DEBUG', 'Running bear LocalTestBear...'),
            ('root', 'WARNING', 'A given local bear (str) is not valid. '
                                'Leaving it out... This is a bug. We are '
                                'sorry for the inconvenience. Please contact '
                                'the developers for assistance.'),
            ('root', 'ERROR', 'An internal error occurred. This is a bug. We '
                              'are sorry for the inconvenience. Please contact '
                              'the developers for assistance.'),
            ('root', 'DEBUG', 'The given file through the queue is not in '
                              'the file dictionary.'),
            ('root', 'DEBUG', 'Running bear GlobalTestBear...'),
            ('root', 'WARNING', 'A given global bear (str) is not valid. '
                                'Leaving it out... This is a bug. We are '
                                'sorry for the inconvenience. Please contact '
                                'the developers for assistance.')
        )

        local_result_expected = [[],
                                 [Result.from_values('LocalTestBear',
                                                     'something went wrong',
                                                     'arbitrary')]
                                 ]
        for expected in local_result_expected:
            control_elem, index = self.control_queue.get()
            self.assertEqual(control_elem, CONTROL_ELEMENT.LOCAL)
            real = self.local_result_dict[index]
            self.assertEqual(real, expected)

        global_results_expected = [Result.from_values(
                                       'GlobalTestBear',
                                       'Files are bad in general!',
                                       'file1',
                                       severity=RESULT_SEVERITY.INFO),
                                   Result.from_values(
                                       'GlobalTestBear',
                                       'Files are bad in general!',
                                       'arbitrary',
                                       severity=RESULT_SEVERITY.INFO)]

        control_elem, index = self.control_queue.get()
        self.assertEqual(control_elem, CONTROL_ELEMENT.LOCAL_FINISHED)
        control_elem, index = self.control_queue.get()
        self.assertEqual(control_elem, CONTROL_ELEMENT.GLOBAL)
        real = self.global_result_dict[index]
        self.assertEqual(sorted(global_results_expected), sorted(real))

        control_elem, none = self.control_queue.get(timeout=0)
        self.assertEqual(control_elem, CONTROL_ELEMENT.GLOBAL_FINISHED)
        self.assertEqual(none, None)

        # The invalid bear gets a None in that dict for dependency resolution
        self.assertEqual(len(self.global_result_dict), 2)
        self.assertEqual(len(self.local_result_dict),
                         len(local_result_expected))
        self.assertRaises(queue.Empty, self.message_queue.get, timeout=0)
        self.assertRaises(queue.Empty, self.control_queue.get, timeout=0)
