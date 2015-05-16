import inspect
import os
import queue
import sys

sys.path.insert(0, ".")
import unittest
from coalib.settings.SectionManager import SectionManager
from coalib.output.Interactor import Interactor
from coalib.output.printers.LogPrinter import LogPrinter
from coalib.processes.SectionExecutor import SectionExecutor
from coalib.output.printers.ConsolePrinter import ConsolePrinter
from coalib.processes.CONTROL_ELEMENT import CONTROL_ELEMENT


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
        assert self.set_up
        self.result_queue.put(result_list)

    def begin_section(self, name):
        self.set_up = True


class ProcessQueuesTestSectionExecutor(SectionExecutor):
    """
    A SectionExecutor class designed to simply test _process_queues on its own.
    """

    def __init__(self,
                 section,
                 local_bear_list,
                 global_bear_list,
                 interactor,
                 log_printer):
        SectionExecutor.__init__(self,
                                 section,
                                 local_bear_list,
                                 global_bear_list,
                                 interactor,
                                 log_printer)

    def process_queues(self,
                       control_queue,
                       local_result_dict,
                       global_result_dict):
        # Pass control_queue as processes
        self._process_queues(control_queue,
                             control_queue,
                             local_result_dict,
                             global_result_dict,
                             None)

    @staticmethod
    def _get_running_processes(processes):
        # Two processes plus one logger process until no commands are left.
        return 0 if processes.empty() else 3


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

        self.sections, self.local_bears, self.global_bears, targets \
            = SectionManager().run(["--config", config_path])[0:4]
        self.assertEqual(len(self.local_bears["default"]), 1)
        self.assertEqual(len(self.global_bears["default"]), 1)
        self.assertEqual(targets, [])

        self.result_queue = queue.Queue()
        self.log_queue = queue.Queue()

        log_printer = ConsolePrinter()
        self.interactor = SectionExecutorTestInteractor(log_printer,
                                                        self.result_queue,
                                                        self.log_queue)

        self.uut = SectionExecutor(self.sections["default"],
                                   self.local_bears["default"],
                                   self.global_bears["default"],
                                   self.interactor,
                                   self.interactor)

    def test_run(self):
        results = self.uut.run()
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
        # We'll get 1 log message per bear (set up, run, tear down) plus one
        # for the unreadable file.
        self.assertEqual(self.log_queue.qsize(), 3)

    def test_empty_run(self):
        self.uut.global_bear_list = []
        self.uut.local_bear_list = []
        results = self.uut.run()
        # No results
        self.assertFalse(results[0])
        # One file
        self.assertEqual(len(results[1]), 1)
        # No global bear
        self.assertEqual(len(results[2]), 0)

    def test_process_queues(self):
        mock_interactor = MessageQueueingInteractor()
        uut = ProcessQueuesTestSectionExecutor(
            self.sections["default"],
            self.local_bears["default"],
            self.global_bears["default"],
            mock_interactor,
            mock_interactor)
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

        uut.process_queues(ctrlq,
                           {1: "The first result.", 2: "The second result."},
                           {1: "The one and only global result."})

        self.assertEqual(mock_interactor.get(), ("The first result.", None))
        self.assertEqual(mock_interactor.get(), ("The second result.", None))
        self.assertEqual(mock_interactor.get(),
                         ("The one and only global result.", None))
        self.assertEqual(mock_interactor.get(),
                         ("The one and only global result.", None))


if __name__ == '__main__':
    unittest.main(verbosity=2)
