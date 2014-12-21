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
import queue
import sys
import multiprocessing

sys.path.insert(0, ".")
import unittest
from coalib.processes.CONTROL_ELEMENT import CONTROL_ELEMENT
from coalib.bears.results.Result import Result, RESULT_SEVERITY
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


class GlobalTestBear(GlobalBear):
    def run_bear(self):
        result = []
        for file, contents in self.file_dict.items():
            result.append(Result("GlobalTestBear",
                                 "Files are bad in general!",
                                 file,
                                 severity=RESULT_SEVERITY.INFO))
        return result


class BearRunnerConstructionTestCase(unittest.TestCase):
    def test_initialization(self):
        file_name_queue = queue.Queue()
        local_bear_list = []
        global_bear_queue = queue.Queue()
        file_dict = {}
        local_result_queue = queue.Queue()
        global_result_queue = queue.Queue()
        message_queue = queue.Queue()
        control_queue = queue.Queue()
        barrier = Barrier(parties=1)
        self.assertRaises(TypeError, BearRunner, 0, local_bear_list, [], global_bear_queue,
                          file_dict, local_result_queue, global_result_queue, message_queue, control_queue, barrier)
        self.assertRaises(TypeError, BearRunner, file_name_queue, 0, [], global_bear_queue,
                          file_dict, local_result_queue, global_result_queue, message_queue, control_queue, barrier)
        self.assertRaises(TypeError, BearRunner, file_name_queue, local_bear_list, 0, global_bear_queue,
                          file_dict, local_result_queue, global_result_queue, message_queue, control_queue, barrier)
        self.assertRaises(TypeError, BearRunner, file_name_queue, local_bear_list, [], 0,
                          file_dict, local_result_queue, global_result_queue, message_queue, control_queue, barrier)
        self.assertRaises(TypeError, BearRunner, file_name_queue, local_bear_list, [], global_bear_queue,
                          0, local_result_queue, global_result_queue, message_queue, control_queue, barrier)
        self.assertRaises(TypeError, BearRunner, file_name_queue, local_bear_list, [],
                          global_bear_queue, file_dict, 0, global_result_queue, message_queue, control_queue, barrier)
        self.assertRaises(TypeError, BearRunner, file_name_queue, local_bear_list, [],
                          global_bear_queue, file_dict, local_result_queue, 0, message_queue, control_queue, barrier)
        self.assertRaises(TypeError, BearRunner, file_name_queue, local_bear_list, [], global_bear_queue,
                          file_dict, local_result_queue, global_result_queue, 0, control_queue, barrier)
        self.assertRaises(TypeError, BearRunner, file_name_queue, local_bear_list, [], global_bear_queue,
                          file_dict, local_result_queue, global_result_queue, message_queue, 0, barrier)
        self.assertRaises(TypeError, BearRunner, file_name_queue, local_bear_list, [], global_bear_queue,
                          file_dict, local_result_queue, global_result_queue, message_queue, control_queue, 0)


class BearRunnerUnitTestCase(unittest.TestCase):
    def setUp(self):
        self.file_name_queue = queue.Queue()
        self.local_bear_list = []
        self.global_bear_list = []
        self.global_bear_queue = queue.Queue()
        self.file_dict = {}
        self.local_result_queue = queue.Queue()
        self.global_result_queue = queue.Queue()
        self.message_queue = queue.Queue()
        self.control_queue = queue.Queue()
        self.barrier = Barrier(parties=1)
        self.uut = BearRunner(self.file_name_queue, self.local_bear_list, self.global_bear_list,
                              self.global_bear_queue, self.file_dict, self.local_result_queue,
                              self.global_result_queue, self.message_queue, self.control_queue, self.barrier)

    def test_inheritance(self):
        self.assertIsInstance(self.uut, multiprocessing.Process)

    def test_messaging(self):
        self.uut.debug("test", "messag", delimiter="-", end="e")
        self.uut.warn("test", "messag", delimiter="-", end="e")
        self.uut.err("test", "messag", delimiter="-", end="e")

        self.assertEqual(self.message_queue.get(), LogMessage(LOG_LEVEL.DEBUG, "test-message"))
        self.assertEqual(self.message_queue.get(), LogMessage(LOG_LEVEL.WARNING, "test-message"))
        self.assertEqual(self.message_queue.get(), LogMessage(LOG_LEVEL.ERROR, "test-message"))


class BearRunnerIntegrationTestCase(BearRunnerUnitTestCase):
    example_file = """a
b
c
d
"""

    def setUp(self):
        BearRunnerUnitTestCase.setUp(self)

        self.file1 = "file1"
        self.file2 = "arbitrary"

        self.settings = Section("name")

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
            real = self.local_result_queue.get(timeout=0)
            for i in range(len(expected)):
                self.assertEqual(real[i], expected[i])

        global_results_expected = [Result("GlobalTestBear", "Files are bad in general!", "file1",
                                          severity=RESULT_SEVERITY.INFO),
                                   Result("GlobalTestBear", "Files are bad in general!", "arbitrary",
                                          severity=RESULT_SEVERITY.INFO)]

        real = self.global_result_queue.get(timeout=0)
        for expected in global_results_expected:
            self.assertTrue(expected in real)

        self.assertEqual(len(real), len(global_results_expected))

        control_queue_expected = [CONTROL_ELEMENT.LOCAL, CONTROL_ELEMENT.LOCAL,
                                  CONTROL_ELEMENT.GLOBAL, CONTROL_ELEMENT.FINISHED]
        for expected in control_queue_expected:
            real = self.control_queue.get(timeout=0)
            self.assertEqual(expected, real)

        self.assertRaises(queue.Empty, self.message_queue.get, timeout=0)
        self.assertRaises(queue.Empty, self.local_result_queue.get, timeout=0)
        self.assertRaises(queue.Empty, self.global_result_queue.get, timeout=0)
        self.assertRaises(queue.Empty, self.control_queue.get, timeout=0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
