import queue
import sys
import multiprocessing

sys.path.insert(0, ".")
import unittest
from coalib.processes.CONTROL_ELEMENT import CONTROL_ELEMENT
from coalib.results.Result import Result, RESULT_SEVERITY
from coalib.bears.LocalBear import LocalBear
from coalib.bears.GlobalBear import GlobalBear
from coalib.processes.BearRunner import BearRunner, LogMessage, LOG_LEVEL
from coalib.processes.Barrier import Barrier
from coalib.settings.Section import Section


class LocalTestBear(LocalBear):
    def run_bear(self, filename, file):
        if filename == "file1":
            raise Exception("Just to throw anything here.")
        return [Result("LocalTestBear", "something went wrong", filename)]


class SimpleBear(LocalBear):
    def run_bear(self,
                 filename,
                 file,
                 *args,
                 dependency_results=None,
                 **kwargs):
        return [Result("SimpleBear", "something went wrong", filename),
                # This result should not be passed to DependentBear
                Result("FakeBear", "something went wrong", filename),
                Result("SimpleBear", "another thing went wrong", filename)]


class DependentBear(LocalBear):
    def run_bear(self,
                 filename,
                 file,
                 *args,
                 dependency_results=None,
                 **kwargs):
        assert len(dependency_results["SimpleBear"]) == 2

        return []

    @staticmethod
    def get_dependencies():
        return [SimpleBear]


class GlobalTestBear(GlobalBear):
    def run_bear(self):
        result = []
        for file, contents in self.file_dict.items():
            result.append(Result("GlobalTestBear",
                                 "Files are bad in general!",
                                 file,
                                 severity=RESULT_SEVERITY.INFO))
        return result


class EvilBear(LocalBear):
    def run(self, *args, **kwargs):
        raise NotImplementedError


class BearRunnerConstructionTestCase(unittest.TestCase):
    def test_initialization(self):
        file_name_queue = queue.Queue()
        local_bear_list = []
        global_bear_queue = queue.Queue()
        file_dict = {}
        manager = multiprocessing.Manager()
        local_result_dict = manager.dict()
        global_result_dict = manager.dict()
        message_queue = queue.Queue()
        control_queue = queue.Queue()
        barrier = Barrier(parties=1)
        self.assertRaises(TypeError, BearRunner, 0, local_bear_list, [], global_bear_queue,
                          file_dict, local_result_dict, global_result_dict, message_queue, control_queue, barrier)
        self.assertRaises(TypeError, BearRunner, file_name_queue, 0, [], global_bear_queue,
                          file_dict, local_result_dict, global_result_dict, message_queue, control_queue, barrier)
        self.assertRaises(TypeError, BearRunner, file_name_queue, local_bear_list, 0, global_bear_queue,
                          file_dict, local_result_dict, global_result_dict, message_queue, control_queue, barrier)
        self.assertRaises(TypeError, BearRunner, file_name_queue, local_bear_list, [], 0,
                          file_dict, local_result_dict, global_result_dict, message_queue, control_queue, barrier)
        self.assertRaises(TypeError, BearRunner, file_name_queue, local_bear_list, [], global_bear_queue,
                          0, local_result_dict, global_result_dict, message_queue, control_queue, barrier)
        self.assertRaises(TypeError, BearRunner, file_name_queue, local_bear_list, [],
                          global_bear_queue, file_dict, 0, global_result_dict, message_queue, control_queue, barrier)
        self.assertRaises(TypeError, BearRunner, file_name_queue, local_bear_list, [],
                          global_bear_queue, file_dict, local_result_dict, 0, message_queue, control_queue, barrier)
        self.assertRaises(TypeError, BearRunner, file_name_queue, local_bear_list, [], global_bear_queue,
                          file_dict, local_result_dict, global_result_dict, 0, control_queue, barrier)
        self.assertRaises(TypeError, BearRunner, file_name_queue, local_bear_list, [], global_bear_queue,
                          file_dict, local_result_dict, global_result_dict, message_queue, 0, barrier)
        self.assertRaises(TypeError, BearRunner, file_name_queue, local_bear_list, [], global_bear_queue,
                          file_dict, local_result_dict, global_result_dict, message_queue, control_queue, 0)


class BearRunnerUnitTestCase(unittest.TestCase):
    def setUp(self):
        self.settings = Section("name")

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
        self.barrier = Barrier(parties=1)
        self.uut = BearRunner(self.file_name_queue, self.local_bear_list, self.global_bear_list,
                              self.global_bear_queue, self.file_dict, self.local_result_dict,
                              self.global_result_dict, self.message_queue, self.control_queue, self.barrier)

    def test_inheritance(self):
        self.assertIsInstance(self.uut, multiprocessing.Process)

    def test_messaging(self):
        self.uut.debug("test", "messag", delimiter="-", end="e")
        self.uut.warn("test", "messag", delimiter="-", end="e")
        self.uut.err("test", "messag", delimiter="-", end="e")

        self.assertEqual(self.message_queue.get(), LogMessage(LOG_LEVEL.DEBUG, "test-message"))
        self.assertEqual(self.message_queue.get(), LogMessage(LOG_LEVEL.WARNING, "test-message"))
        self.assertEqual(self.message_queue.get(), LogMessage(LOG_LEVEL.ERROR, "test-message"))

    def test_dependencies(self):
        self.local_bear_list.append(SimpleBear(self.settings,
                                               self.message_queue))
        self.local_bear_list.append(DependentBear(self.settings,
                                                  self.message_queue))
        self.file_name_queue.put("t")
        self.file_dict["t"] = []

        self.uut.run()

        try:
            while True:
                msg = self.message_queue.get(timeout=0)
                self.assertEqual(msg.log_level, LOG_LEVEL.DEBUG)
        except queue.Empty:
            pass

    def test_evil_bear(self):
        self.local_bear_list.append(EvilBear(self.settings,
                                             self.message_queue))
        self.file_name_queue.put("t")
        self.file_dict["t"] = []

        self.uut.run()


class BearRunnerIntegrationTestCase(unittest.TestCase):
    example_file = """a
b
c
d
"""

    def setUp(self):
        self.settings = Section("name")

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
        self.barrier = Barrier(parties=1)
        self.uut = BearRunner(self.file_name_queue,
                              self.local_bear_list,
                              self.global_bear_list,
                              self.global_bear_queue,
                              self.file_dict,
                              self.local_result_dict,
                              self.global_result_dict,
                              self.message_queue,
                              self.control_queue,
                              self.barrier)

        self.file1 = "file1"
        self.file2 = "arbitrary"

        self.file_name_queue.put(self.file1)
        self.file_name_queue.put(self.file2)
        self.file_name_queue.put("invalid file")
        self.local_bear_list.append(LocalTestBear(self.settings, self.message_queue))
        self.local_bear_list.append("not a valid bear")
        self.file_dict[self.file1] = self.example_file
        self.file_dict[self.file2] = self.example_file
        self.global_bear_list.append(GlobalTestBear(self.file_dict, self.settings, self.message_queue))
        self.global_bear_list.append("not a valid bear")
        self.global_bear_queue.put(0)
        self.global_bear_queue.put(1)

    def test_run(self):
        self.uut.run()

        expected_messages = [LOG_LEVEL.DEBUG,
                             LOG_LEVEL.DEBUG,
                             LOG_LEVEL.WARNING,
                             LOG_LEVEL.DEBUG,
                             LOG_LEVEL.WARNING,
                             LOG_LEVEL.DEBUG,
                             LOG_LEVEL.DEBUG,
                             LOG_LEVEL.DEBUG,
                             LOG_LEVEL.WARNING,
                             LOG_LEVEL.ERROR,
                             LOG_LEVEL.DEBUG,
                             LOG_LEVEL.DEBUG,
                             LOG_LEVEL.DEBUG,
                             LOG_LEVEL.DEBUG,
                             LOG_LEVEL.WARNING]
        for msg in expected_messages:
            self.assertEqual(msg, self.message_queue.get(timeout=0).log_level)

        local_result_expected = [[],
                                 [Result("LocalTestBear", "something went wrong", 'arbitrary')]
                                ]
        for expected in local_result_expected:
            control_elem, index = self.control_queue.get()
            self.assertEqual(control_elem, CONTROL_ELEMENT.LOCAL)
            real = self.local_result_dict[index]
            self.assertEqual(real, expected)

        global_results_expected = [Result("GlobalTestBear", "Files are bad in general!", "file1",
                                          severity=RESULT_SEVERITY.INFO),
                                   Result("GlobalTestBear", "Files are bad in general!", "arbitrary",
                                          severity=RESULT_SEVERITY.INFO)]


        control_elem, index = self.control_queue.get()
        self.assertEqual(control_elem, CONTROL_ELEMENT.GLOBAL)
        real = self.global_result_dict[index]
        self.assertEqual(sorted(global_results_expected), sorted(real))

        control_elem, none = self.control_queue.get(timeout=0)
        self.assertEqual(control_elem, CONTROL_ELEMENT.FINISHED)
        self.assertEqual(none, None)

        # The invalid bear gets a None in that dict for dependency resolution
        self.assertEqual(len(self.global_result_dict), 2)
        self.assertEqual(len(self.local_result_dict),
                         len(local_result_expected))
        self.assertRaises(queue.Empty, self.message_queue.get, timeout=0)
        self.assertRaises(queue.Empty, self.control_queue.get, timeout=0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
