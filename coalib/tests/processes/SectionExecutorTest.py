import inspect
import os
import queue
import unittest
import sys
import multiprocessing

sys.path.insert(0, ".")
from coalib.results.HiddenResult import HiddenResult
from coalib.settings.ConfigurationGathering import gather_configuration
from coalib.output.Interactor import Interactor
from coalib.output.printers.LogPrinter import LogPrinter
from coalib.processes.SectionExecutor import execute_section
from coalib.output.printers.ConsolePrinter import ConsolePrinter
from coalib.processes.CONTROL_ELEMENT import CONTROL_ELEMENT
from coalib.processes.SectionExecutor import process_queues
import re


class DummyProcess(multiprocessing.Process):
    def __init__(self, ctrlq):
        multiprocessing.Process.__init__(self)
        self.control_queue = ctrlq

    def is_alive(self):
        if self.control_queue.empty():
            return False
        return True


class SectionExecutorTestInteractor(Interactor, LogPrinter):
    def __init__(self, log_printer, result_queue, log_queue):
        Interactor.__init__(self, log_printer)
        LogPrinter.__init__(self)
        self.result_queue = result_queue
        self.log_queue = log_queue
        self.set_up = False

    def log_message(self, log_message, timestamp=None, **kwargs):
        self.log_queue.put(log_message)

    def print_results(self, result_list, file_dict):
        self.result_queue.put(result_list)


class MessageQueueingInteractor(Interactor):
    """
    A simple interactor that pushes all results it gets to a queue for
    testing purposes.
    """

    def __init__(self):
        Interactor.__init__(self, None)
        self.queue = queue.Queue()

    def print_results(self, *args):
        self.queue.put(args)

    def get(self):
        return self.queue.get(timeout=0)


class SectionExecutorTest(unittest.TestCase):
    def setUp(self):
        config_path = os.path.abspath(os.path.join(
            os.path.dirname(inspect.getfile(SectionExecutorTest)),
            "section_executor_test_files",
            ".coafile"))
        self.testcode_c_path = os.path.join(os.path.dirname(config_path),
                                            "testcode.c")

        self.sections, self.local_bears, self.global_bears, targets = (
            gather_configuration(["--config", re.escape(config_path)])[0:4])
        self.assertEqual(len(self.local_bears["default"]), 1)
        self.assertEqual(len(self.global_bears["default"]), 1)
        self.assertEqual(targets, [])

        self.result_queue = queue.Queue()
        self.log_queue = queue.Queue()

        log_printer = ConsolePrinter()
        self.interactor = SectionExecutorTestInteractor(log_printer,
                                                        self.result_queue,
                                                        self.log_queue)

    def test_run(self):
        results = execute_section(self.sections["default"],
                                  self.global_bears["default"],
                                  self.local_bears["default"],
                                  self.interactor,
                                  self.interactor)
        self.assertTrue(results[0])

        local_results = self.result_queue.get(timeout=0)
        global_results = self.result_queue.get(timeout=0)
        self.assertTrue(self.result_queue.empty())

        self.assertEqual(len(local_results), 1)
        self.assertEqual(len(global_results), 1)
        # Result dict also returned
        # One file
        self.assertEqual(len(results[1]), 1)
        # One global bear
        self.assertEqual(len(results[2]), 1)

        local_result = local_results[0]
        global_result = global_results[0]

        self.assertEqual(str(local_result),
                         "Result:\n origin: 'LocalTestBear'\n file: 'None'\n "
                         "line nr: None\n severity: 1\n'test msg'")
        self.assertEqual(str(global_result),
                         "Result:\n origin: 'GlobalTestBear'\n file: '{file}'"
                         "\n line nr: None\n severity: 1\n'test "
                         "message'".format(file=self.testcode_c_path))

        # Checking the content of those messages would mean checking hardcoded
        # strings. I recall some other test already does this so we
        # shouldn't make maintenance so hard for us here.

    def test_empty_run(self):
        results = execute_section(self.sections["default"],
                                  [],
                                  [],
                                  self.interactor,
                                  self.interactor)
        # No results
        self.assertFalse(results[0])
        # One file
        self.assertEqual(len(results[1]), 1)
        # No global bear
        self.assertEqual(len(results[2]), 0)

    def test_process_queues(self):
        mock_interactor = MessageQueueingInteractor()
        ctrlq = queue.Queue()

        # Append custom controlling sequences.

        # Simulated process 1
        ctrlq.put((CONTROL_ELEMENT.LOCAL, 1))
        ctrlq.put((CONTROL_ELEMENT.LOCAL_FINISHED, None))
        ctrlq.put((CONTROL_ELEMENT.GLOBAL, 1))

        # Simulated process 2
        ctrlq.put((CONTROL_ELEMENT.LOCAL, 2))

        # Simulated process 1
        ctrlq.put((CONTROL_ELEMENT.GLOBAL_FINISHED, None))

        # Simulated process 2
        ctrlq.put((CONTROL_ELEMENT.LOCAL_FINISHED, None))
        ctrlq.put((CONTROL_ELEMENT.GLOBAL, 1))
        ctrlq.put((CONTROL_ELEMENT.GLOBAL_FINISHED, None))

        process_queues(
            mock_interactor,
            [DummyProcess(ctrlq=ctrlq) for i in range(3)],
            ctrlq,
            {1: ["The first result."],
             2: ["The second result.", HiddenResult("t", "c")]},
            {1: ["The one and only global result."]},
            None)

        self.assertEqual(mock_interactor.get(), (["The first result."], None))
        self.assertEqual(mock_interactor.get(), (["The second result."], None))
        self.assertEqual(mock_interactor.get(),
                         (["The one and only global result."], None))
        self.assertEqual(mock_interactor.get(),
                         (["The one and only global result."], None))

        # No valid FINISH element in the queue
        ctrlq.put((CONTROL_ELEMENT.GLOBAL_FINISHED, None))

        process_queues(
            mock_interactor,
            [DummyProcess(ctrlq=ctrlq) for i in range(3)],
            ctrlq,
            {1: "The first result.", 2: "The second result."},
            {1: "The one and only global result."},
            None)
        with self.assertRaises(queue.Empty):
            mock_interactor.get()


if __name__ == '__main__':
    unittest.main(verbosity=2)
