"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
import inspect
import os
import queue
import sys
sys.path.insert(0, ".")
import unittest
from coalib.settings.SectionManager import SectionManager
from coalib.output.Outputter import Outputter
from coalib.output.LogPrinter import LogPrinter
from coalib.processes.SectionExecutor import SectionExecutor
from coalib.settings.Section import Section


class SectionExecutorTestOutputter(Outputter, LogPrinter):
    def __init__(self, result_queue, log_queue):
        Outputter.__init__(self)
        self.result_queue = result_queue
        self.log_queue = log_queue

    def log_message(self, log_message, timestamp=None, **kwargs):
        self.log_queue.put(log_message)

    def print_results(self, result_list, file_dict):
        self.result_queue.put(result_list)


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

        self.sections, self.local_bears, self.global_bears = SectionManager().run(["--config", config_path])
        self.assertEqual(len(self.local_bears["default"]), 1)
        self.assertEqual(len(self.global_bears["default"]), 1)

        self.result_queue = queue.Queue()
        self.log_queue = queue.Queue()

        self.outputter = SectionExecutorTestOutputter(self.result_queue, self.log_queue)

        self.sections["default"].outputter = self.outputter
        self.sections["default"].log_printer = self.outputter
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
                         "Result:\n origin: 'LocalTestBear'\n file: 'None'\n severity: 1\n'test message'")
        self.assertEqual(str(global_result),
                         "Result:\n origin: 'GlobalTestBear'\n file: "
                         "'{file}'\n severity: 1\n'test message'".format(file=self.testcode_c_path))

        # Checking the content of those messages would mean checking hardcoded strings. I recall some other test already
        # does this so we shouldn't make maintenance so hard for us here.
        self.assertEqual(self.log_queue.qsize(), 6)  # 3 log messages per bear (set up, run, tear down)


if __name__ == '__main__':
    unittest.main(verbosity=2)
