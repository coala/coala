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
import os
import queue
import sys
import tempfile

sys.path.insert(0, ".")
import unittest
from coalib.analysers.results.Result import Result, RESULT_SEVERITY
from coalib.analysers.LocalAnalyzer import LocalAnalyzer
from coalib.analysers.GlobalAnalyzer import GlobalAnalyzer
from coalib.processes.AnalyzerRunProcess import AnalyzerRunProcess, LogMessage, LOG_LEVEL
from coalib.settings.Settings import Settings


class LocalTestAnalyzer(LocalAnalyzer):
    def run_analyser(self, filename, file):
        if filename == "file1":
            raise Exception("Just to throw anything here.")
        return [Result("LocalTestAnalyzer", "something went wrong", filename)]


class GlobalTestAnalyzer(GlobalAnalyzer):
    def run_analyser(self):
        result = []
        for file, contents in self.file_dict.items():
            result.append(Result("GlobalTestAnalyzer",
                                 "Files are bad in general!",
                                 file,
                                 severity=RESULT_SEVERITY.INFO))
        return result


class AnalyzerRunProcessConstructionTestCase(unittest.TestCase):
    def test_initialization(self):
        file_name_queue = queue.Queue()
        local_analyzer_list = []
        global_analyzer_queue = queue.Queue()
        file_dict = {}
        local_result_queue = queue.Queue()
        global_result_queue = queue.Queue()
        message_queue = queue.Queue()
        self.assertRaises(TypeError, AnalyzerRunProcess, 0, local_analyzer_list,
                          global_analyzer_queue, file_dict, local_result_queue, global_result_queue, message_queue)
        self.assertRaises(TypeError, AnalyzerRunProcess, file_name_queue, 0,
                          global_analyzer_queue, file_dict, local_result_queue, global_result_queue, message_queue)
        self.assertRaises(TypeError, AnalyzerRunProcess, file_name_queue, local_analyzer_list,
                          0, file_dict, local_result_queue, global_result_queue, message_queue)
        self.assertRaises(TypeError, AnalyzerRunProcess, file_name_queue, local_analyzer_list,
                          global_analyzer_queue, 0, local_result_queue, global_result_queue, message_queue)
        self.assertRaises(TypeError, AnalyzerRunProcess, file_name_queue, local_analyzer_list,
                          global_analyzer_queue, file_dict, 0, global_result_queue, message_queue)
        self.assertRaises(TypeError, AnalyzerRunProcess, file_name_queue, local_analyzer_list,
                          global_analyzer_queue, file_dict, local_result_queue, 0, message_queue)
        self.assertRaises(TypeError, AnalyzerRunProcess, file_name_queue, local_analyzer_list,
                          global_analyzer_queue, file_dict, local_result_queue, global_result_queue, 0)


class AnalyzerRunProcessUnitTestCase(unittest.TestCase):
    def setUp(self):
        self.file_name_queue = queue.Queue()
        self.local_analyzer_list = []
        self.global_analyzer_queue = queue.Queue()
        self.file_dict = {}
        self.local_result_queue = queue.Queue()
        self.global_result_queue = queue.Queue()
        self.message_queue = queue.Queue()
        self.uut = AnalyzerRunProcess(self.file_name_queue, self.local_analyzer_list, self.global_analyzer_queue,
                                      self.file_dict, self.local_result_queue, self.global_result_queue,
                                      self.message_queue)

    def test_messaging(self):
        self.uut.debug("test", "messag", delimiter="-", end="e")
        self.uut.warn("test", "messag", delimiter="-", end="e")
        self.uut.err("test", "messag", delimiter="-", end="e")

        self.assertEqual(self.message_queue.get(), LogMessage(LOG_LEVEL.DEBUG, "test-message"))
        self.assertEqual(self.message_queue.get(), LogMessage(LOG_LEVEL.WARNING, "test-message"))
        self.assertEqual(self.message_queue.get(), LogMessage(LOG_LEVEL.ERROR, "test-message"))


class AnalyzerRunProcessIntegrationTestCase(AnalyzerRunProcessUnitTestCase):
    example_file = """a
b
c
d
"""
    def setUp(self):
        AnalyzerRunProcessUnitTestCase.setUp(self)

        self.file1 = "file1"
        self.file2 = "arbitrary"

        self.settings = Settings("name")

        self.file_name_queue.put(self.file1)
        self.file_name_queue.put(self.file2)
        self.file_name_queue.put("invalid file")
        self.local_analyzer_list.append(LocalTestAnalyzer(self.settings, self.message_queue))
        self.local_analyzer_list.append("not a valid analyzer")
        self.file_dict[self.file1] = self.example_file
        self.file_dict[self.file2] = self.example_file
        self.global_analyzer_queue.put(GlobalTestAnalyzer(self.file_dict, self.settings, self.message_queue))
        self.global_analyzer_queue.put("not a valid analyzer")

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

        local_result_expected = [('file1', {}),
                                 ('arbitrary', {'LocalTestAnalyzer': Result("LocalTestAnalyzer",
                                                                            "something went wrong",
                                                                            'arbitrary')})]
        for firste, seconde in local_result_expected:
            first, second = self.local_result_queue.get(timeout=0)
            self.assertEqual(first, firste)
            self.assertEqual(second.keys(), seconde.keys())

        global_results_expected = [("GlobalTestAnalyzer",
                                    [Result("GlobalTestAnalyzer", "Files are bad in general!", "file1",
                                     severity=RESULT_SEVERITY.INFO),
                                     Result("GlobalTestAnalyzer", "Files are bad in general!", "arbitrary",
                                     severity=RESULT_SEVERITY.INFO)]
                                   )]
        for firste, seconde in global_results_expected:
            first, second = self.global_result_queue.get(timeout=0)
            self.assertEqual(first, firste)
            for elem in second:
                if not elem in seconde:
                    self.assertTrue(False)
            self.assertEqual(len(seconde), len(second))

        self.assertRaises(queue.Empty, self.message_queue.get, timeout=0)
        self.assertRaises(queue.Empty, self.local_result_queue.get, timeout=0)
        self.assertRaises(queue.Empty, self.global_result_queue.get, timeout=0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
