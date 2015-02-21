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
from coalib.settings.Section import Section


class SectionExecutorTestInteractor(Interactor, LogPrinter):
    def __init__(self, result_queue, log_queue):
        Interactor.__init__(self)
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


class SectionExecutorInitTestCase(unittest.TestCase):
    def test_init(self):
        self.assertRaises(TypeError, SectionExecutor, 5,               [], [])
        self.assertRaises(TypeError, SectionExecutor, Section("test"), 5 , [])
        self.assertRaises(TypeError, SectionExecutor, Section("test"), [], 5 )
        self.assertRaises(IndexError, SectionExecutor(Section("test"), [], []).run)


class SectionExecutorTestCase(unittest.TestCase):
    def setUp(self):
        config_path = os.path.abspath(os.path.join(os.path.dirname(inspect.getfile(SectionExecutorTestCase)),
                                                   "section_executor_test_files",
                                                   ".coafile"))
        self.testcode_c_path = os.path.join(os.path.dirname(config_path), "testcode.c")

        self.sections, self.local_bears, self.global_bears, targets =\
            SectionManager().run(["--config", config_path])
        self.assertEqual(len(self.local_bears["default"]), 1)
        self.assertEqual(len(self.global_bears["default"]), 1)
        self.assertEqual(targets, [])

        self.result_queue = queue.Queue()
        self.log_queue = queue.Queue()

        self.interactor = SectionExecutorTestInteractor(self.result_queue, self.log_queue)

        self.sections["default"].interactor = self.interactor
        self.sections["default"].log_printer = self.interactor
        self.uut = SectionExecutor(self.sections["default"], self.local_bears["default"], self.global_bears["default"])

    def test_run(self):
        self.uut.run()

        local_results  = self.result_queue.get(timeout=0)
        global_results = self.result_queue.get(timeout=0)
        self.assertTrue(self.result_queue.empty())

        self.assertEqual(len(local_results), 1)
        self.assertEqual(len(global_results), 1)

        local_result  = local_results[0]
        global_result = global_results[0]

        self.assertEqual(str(local_result),
                         "Result:\n origin: 'LocalTestBear'\n file: 'None'\n line nr: None\n severity: 1\n'test msg'")
        self.assertEqual(str(global_result),
                         "Result:\n origin: 'GlobalTestBear'\n file: "
                         "'{file}'\n line nr: None\n severity: 1\n'test message'".format(file=self.testcode_c_path))

        # Checking the content of those messages would mean checking hardcoded strings. I recall some other test already
        # does this so we shouldn't make maintenance so hard for us here.
        self.assertEqual(self.log_queue.qsize(), 6)  # 3 log messages per bear (set up, run, tear down)


if __name__ == '__main__':
    unittest.main(verbosity=2)
