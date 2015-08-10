import queue
import sys
import multiprocessing
import threading

sys.path.insert(0, ".")
import unittest
from coalib.processes.CONTROL_ELEMENT import CONTROL_ELEMENT
from coalib.results.Result import Result, RESULT_SEVERITY
from coalib.bears.LocalBear import LocalBear
from coalib.bears.GlobalBear import GlobalBear
from coalib.processes.BearRunning import (run,
                                          LogMessage,
                                          LOG_LEVEL,
                                          send_msg,
                                          task_done)
from coalib.settings.Section import Section


class LocalTestBear(LocalBear):
    def run(self, filename, file):
        if filename == "file1":
            raise Exception("Just to throw anything here.")
        return [Result("LocalTestBear", "something went wrong", filename)]


class SimpleBear(LocalBear):
    def run(self,
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
    def run(self,
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


class SimpleGlobalBear(GlobalBear):
    def run(self,
            *args,
            dependency_results=None,
            **kwargs):
        return [Result("SimpleGlobalBear", "something went wrong"),
                # This result should not be passed to DependentBear
                Result("FakeBear", "something went wrong"),
                Result("SimpleGlobalBear", "another thing went wrong")]


class DependentGlobalBear(GlobalBear):
    def run(self,
            *args,
            dependency_results=None,
            **kwargs):
        assert len(dependency_results["SimpleGlobalBear"]) == 3

    @staticmethod
    def get_dependencies():
        return [SimpleGlobalBear]


class GlobalTestBear(GlobalBear):
    def run(self):
        result = []
        for file, contents in self.file_dict.items():
            result.append(Result("GlobalTestBear",
                                 "Files are bad in general!",
                                 file,
                                 severity=RESULT_SEVERITY.INFO))
        return result


class EvilBear(LocalBear):
    def execute(self, *args, **kwargs):
        raise NotImplementedError


class UnexpectedBear1(LocalBear):
    def run(self, filename, file):
        return [1,
                Result("UnexpectedBear1", "test result")]


class UnexpectedBear2(LocalBear):
    def run(self, filename, file):
        return 1


class LockingBear(LocalBear):
    def __init__(self, settings, message_q, lock_event, is_waiting_event=None):
        LocalBear.__init__(self, settings, message_q)
        self._lock_event = lock_event
        self._is_waiting_event = is_waiting_event
        self.was_executed = False

    def run(self, filename, file):
        if self._is_waiting_event:
            self._is_waiting_event.set()
        self._lock_event.wait()
        self.was_executed = True


class GlobalLockingBear(GlobalBear):
    def __init__(self,
                 file_dict,
                 settings,
                 message_q,
                 lock_event,
                 is_waiting_event=None):
        GlobalBear.__init__(self, file_dict, settings, message_q)
        self._lock_event = lock_event
        self._is_waiting_event = is_waiting_event
        self.was_executed = False

    def run(self):
        if self._is_waiting_event:
            self._is_waiting_event.set()
        self._lock_event.wait()
        self.was_executed = True


class BearRunningUnitTest(unittest.TestCase):
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
        self.cancel_event = multiprocessing.Event()

    def test_queue_done_marking(self):
        self.message_queue.put("test")
        task_done(self.message_queue)  # Should make the queue joinable
        self.message_queue.join()

        task_done("test")  # Should pass silently

    def test_messaging(self):
        send_msg(self.message_queue,
                 0,
                 LOG_LEVEL.DEBUG,
                 "test",
                 "messag",
                 delimiter="-",
                 end="e")

        self.assertEqual(self.message_queue.get(),
                         LogMessage(LOG_LEVEL.DEBUG, "test-message"))

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
        self.file_name_queue.put("t")
        self.file_dict["t"] = []

        run(self.file_name_queue,
            self.local_bear_list,
            self.global_bear_list,
            self.global_bear_queue,
            self.file_dict,
            self.local_result_dict,
            self.global_result_dict,
            self.message_queue,
            self.control_queue,
            self.cancel_event)

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

        run(self.file_name_queue,
            self.local_bear_list,
            self.global_bear_list,
            self.global_bear_queue,
            self.file_dict,
            self.local_result_dict,
            self.global_result_dict,
            self.message_queue,
            self.control_queue,
            self.cancel_event)

    def test_strange_bear(self):
        self.local_bear_list.append(UnexpectedBear1(self.settings,
                                                    self.message_queue))
        self.local_bear_list.append(UnexpectedBear2(self.settings,
                                                    self.message_queue))
        self.file_name_queue.put("t")
        self.file_dict["t"] = []

        run(self.file_name_queue,
            self.local_bear_list,
            self.global_bear_list,
            self.global_bear_queue,
            self.file_dict,
            self.local_result_dict,
            self.global_result_dict,
            self.message_queue,
            self.control_queue,
            self.cancel_event)

        expected_messages = [LOG_LEVEL.DEBUG,
                             LOG_LEVEL.ERROR,
                             LOG_LEVEL.DEBUG,
                             LOG_LEVEL.DEBUG,
                             LOG_LEVEL.ERROR,
                             LOG_LEVEL.DEBUG]

        for msg in expected_messages:
            self.assertEqual(msg, self.message_queue.get(timeout=0).log_level)

    def test_event_interrupt(self):
        short_run = lambda: run(self.file_name_queue,
                                self.local_bear_list,
                                self.global_bear_list,
                                self.global_bear_queue,
                                self.file_dict,
                                self.local_result_dict,
                                self.global_result_dict,
                                self.message_queue,
                                self.control_queue,
                                self.cancel_event)

        # Normal test without cancel-event.
        unlock_event = multiprocessing.Event()
        wait_event = multiprocessing.Event()
        self.file_dict = {"0": None, "1": None}
        self.local_bear_list = [LockingBear(self.settings,
                                            self.message_queue,
                                            unlock_event,
                                            wait_event)]
        for key in self.file_dict:
            self.file_name_queue.put(key)

        thread = threading.Thread(target=short_run)
        thread.start()

        wait_event.wait()
        unlock_event.set()

        thread.join()

        for bear in self.local_bear_list:
            self.assertTrue(bear.was_executed, True)

        self.assertRaises(queue.Empty, self.file_name_queue.get, block=False)

        # Test with cancel-event.
        unlock_event = multiprocessing.Event()
        wait_event = multiprocessing.Event()
        self.cancel_event = multiprocessing.Event()
        self.local_bear_list = [LockingBear(self.settings,
                                            self.message_queue,
                                            unlock_event,
                                            wait_event)]
        for key in self.file_dict:
            self.file_name_queue.put(key)

        thread = threading.Thread(target=short_run)
        thread.start()

        wait_event.wait()
        self.cancel_event.set()
        unlock_event.set()

        thread.join()

        for bear in self.local_bear_list:
            self.assertTrue(bear.was_executed, True)

        remaining_files = []
        while not self.file_name_queue.empty():
            remaining_files.append(self.file_name_queue.get(timeout=0.1))
        remaining_files.sort()

        self.assertTrue(remaining_files == ["0"] or remaining_files == ["1"])

        # Test cancel-event with global bears.
        unlock_event = multiprocessing.Event()
        is_waiting_event1 = multiprocessing.Event()
        self.local_bear_list = []
        self.global_bear_list = [GlobalLockingBear({},
                                                   self.settings,
                                                   self.message_queue,
                                                   unlock_event,
                                                   is_waiting_event1),
                                 GlobalLockingBear({},
                                                   self.settings,
                                                   self.message_queue,
                                                   unlock_event)]
        self.global_bear_queue.put(0)
        self.global_bear_queue.put(1)
        self.cancel_event = multiprocessing.Event()

        thread = threading.Thread(target=short_run)
        thread.start()

        is_waiting_event1.wait()
        self.cancel_event.set()
        unlock_event.set()

        thread.join()

        self.assertTrue(self.global_bear_list[0].was_executed)
        self.assertFalse(self.global_bear_list[1].was_executed)


class BearRunningIntegrationTest(unittest.TestCase):
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
        self.cancel_event = multiprocessing.Event()

        self.file1 = "file1"
        self.file2 = "arbitrary"

        self.file_name_queue.put(self.file1)
        self.file_name_queue.put(self.file2)
        self.file_name_queue.put("invalid file")
        self.local_bear_list.append(LocalTestBear(self.settings,
                                                  self.message_queue))
        self.local_bear_list.append("not a valid bear")
        self.file_dict[self.file1] = self.example_file
        self.file_dict[self.file2] = self.example_file
        self.global_bear_list.append(GlobalTestBear(self.file_dict,
                                                    self.settings,
                                                    self.message_queue))
        self.global_bear_list.append("not a valid bear")
        self.global_bear_queue.put(0)
        self.global_bear_queue.put(1)

    def test_run(self):
        run(self.file_name_queue,
            self.local_bear_list,
            self.global_bear_list,
            self.global_bear_queue,
            self.file_dict,
            self.local_result_dict,
            self.global_result_dict,
            self.message_queue,
            self.control_queue,
            self.cancel_event)

        expected_messages = [LOG_LEVEL.DEBUG,
                             LOG_LEVEL.WARNING,
                             LOG_LEVEL.DEBUG,
                             LOG_LEVEL.WARNING,
                             LOG_LEVEL.DEBUG,
                             LOG_LEVEL.WARNING,
                             LOG_LEVEL.ERROR,
                             LOG_LEVEL.DEBUG,
                             LOG_LEVEL.DEBUG,
                             LOG_LEVEL.WARNING]
        for msg in expected_messages:
            self.assertEqual(msg, self.message_queue.get(timeout=0).log_level)

        local_result_expected = [[],
                                 [Result("LocalTestBear",
                                         "something went wrong",
                                         'arbitrary')]
                                ]
        for expected in local_result_expected:
            control_elem, index = self.control_queue.get()
            self.assertEqual(control_elem, CONTROL_ELEMENT.LOCAL)
            real = self.local_result_dict[index]
            self.assertEqual(real, expected)

        global_results_expected = [Result("GlobalTestBear",
                                          "Files are bad in general!",
                                          "file1",
                                          severity=RESULT_SEVERITY.INFO),
                                   Result("GlobalTestBear",
                                          "Files are bad in general!",
                                          "arbitrary",
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


if __name__ == '__main__':
    unittest.main(verbosity=2)
