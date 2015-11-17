import os
import queue
import unittest
import sys
import multiprocessing
import platform
import re
import subprocess
from pyprint.ConsolePrinter import ConsolePrinter

sys.path.insert(0, ".")
from coalib.results.HiddenResult import HiddenResult
from coalib.results.Result import Result, RESULT_SEVERITY
from coalib.settings.ConfigurationGathering import gather_configuration
from coalib.output.printers.LogPrinter import LogPrinter
from coalib.processes.Processing import execute_section
from coalib.processes.CONTROL_ELEMENT import CONTROL_ELEMENT
from coalib.processes.Processing import process_queues, create_process_group
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


process_group_test_code = """
import time, subprocess, os, platform, sys;
p=subprocess.Popen([sys.executable,
                  "-c",
                  "import time; time.sleep(0.1)"]);
pgid = p.pid if platform.system() == "Windows" else os.getpgid(p.pid);
print(p.pid, pgid)
p.terminate()
"""


class DummyProcess(multiprocessing.Process):
    def __init__(self, control_queue):
        multiprocessing.Process.__init__(self)
        self.control_queue = control_queue

    def is_alive(self):
        return not self.control_queue.empty()


class ProcessingTestLogPrinter(LogPrinter):
    def __init__(self, log_queue):
        LogPrinter.__init__(self, self)
        self.log_queue = log_queue
        self.set_up = False

    def log_message(self, log_message, timestamp=None, **kwargs):
        self.log_queue.put(log_message)


class ProcessingTest(unittest.TestCase):
    def setUp(self):
        config_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            "section_executor_test_files",
            ".coafile"))
        self.testcode_c_path = os.path.join(os.path.dirname(config_path),
                                            "testcode.c")

        self.result_queue = queue.Queue()
        self.queue = queue.Queue()
        self.log_queue = queue.Queue()
        log_printer = LogPrinter(ConsolePrinter())
        self.log_printer = ProcessingTestLogPrinter(self.log_queue)

        (self.sections,
         self.local_bears,
         self.global_bears,
         targets) = gather_configuration(lambda *args: True,
                                         log_printer,
                                         ["--config", re.escape(config_path)])
        self.assertEqual(len(self.local_bears["default"]), 1)
        self.assertEqual(len(self.global_bears["default"]), 1)
        self.assertEqual(targets, [])

    def test_run(self):
        self.sections['default'].append(Setting('jobs', "1"))
        results = execute_section(self.sections["default"],
                                  self.global_bears["default"],
                                  self.local_bears["default"],
                                  lambda *args: self.result_queue.put(args[2]),
                                  self.log_printer)
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

        self.assertRegex(repr(local_result),
                         "<Result object\\(id={}, origin='LocalTestBear', "
                         "affected_code=\\(\\), severity=NORMAL, message='test "
                         "msg'\\) at 0x[0-9a-fA-F]+>".format(local_result.id))
        self.assertRegex(repr(global_result),
                         "<Result object\\(id={}, origin='GlobalTestBear', affe"
                         "cted_code=\\(.*start=.*file=.*section_executor_test_f"
                         "iles.*line=None.*end=.*\\), severity=NORMAL, message="
                         "'test message'\\) at "
                         "0x[0-9a-fA-F]+>".format(global_result.id))

    def test_empty_run(self):
        self.sections['default'].append(Setting('jobs', "bogus!"))
        results = execute_section(self.sections["default"],
                                  [],
                                  [],
                                  lambda *args: self.result_queue.put(args[2]),
                                  self.log_printer)
        # No results
        self.assertFalse(results[0])
        # One file
        self.assertEqual(len(results[1]), 1)
        # No global bear
        self.assertEqual(len(results[2]), 0)

    def test_process_queues(self):
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

        first_local = Result.from_values("o", "The first result.", file="f")
        second_local = Result.from_values("ABear",
                                          "The second result.",
                                          file="f",
                                          line=1)
        third_local = Result.from_values("ABear",
                                          "The second result.",
                                          file="f",
                                          line=4)
        fourth_local = Result.from_values("ABear",
                                          "Another result.",
                                          file="f",
                                          line=7)
        first_global = Result("o", "The one and only global result.")
        section = Section("")
        section.append(Setting('min_severity', "normal"))
        process_queues(
            [DummyProcess(control_queue=ctrlq) for i in range(3)],
            ctrlq,
            {1: [first_local,
                 second_local,
                 third_local,
                 # The following are to be ignored
                 Result('o', 'm', severity=RESULT_SEVERITY.INFO),
                 Result.from_values("ABear", "u", file="f", line=2),
                 Result.from_values("ABear", "u", file="f", line=3)],
             2: [fourth_local,
                 # The following are to be ignored
                 HiddenResult("t", "c"),
                 Result.from_values("ABear", "u", file="f", line=5),
                 Result.from_values("ABear", "u", file="f", line=6)]},
            {1: [first_global]},
            {"f": ["first line  # stop ignoring, invalid ignore range\n",
                   "second line  # ignore all\n",
                   "third line\n",
                   "fourth line\n",
                   "# Start ignoring ABear, BBear and CBear\n",
                   "# Stop ignoring\n",
                   "seventh"]},
            lambda *args: self.queue.put(args[2]),
            section,
            self.log_printer)

        self.assertEqual(self.queue.get(timeout=0), ([first_local,
                                                      second_local,
                                                      third_local]))
        self.assertEqual(self.queue.get(timeout=0), ([fourth_local]))
        self.assertEqual(self.queue.get(timeout=0), ([first_global]))
        self.assertEqual(self.queue.get(timeout=0), ([first_global]))

        # No valid FINISH element in the queue
        ctrlq.put((CONTROL_ELEMENT.GLOBAL_FINISHED, None))

        process_queues(
            [DummyProcess(control_queue=ctrlq) for i in range(3)],
            ctrlq,
            {1: "The first result.", 2: "The second result."},
            {1: "The one and only global result."},
            {},
            lambda *args: self.queue.put(args[2]),
            Section(""),
            self.log_printer)
        with self.assertRaises(queue.Empty):
            self.queue.get(timeout=0)

    def test_create_process_group(self):
        p = create_process_group([sys.executable,
                                  "-c",
                                  process_group_test_code],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        retval = p.wait()
        if retval != 0:
            for line in p.stderr:
                print(line, end='')
            raise Exception("Subprocess did not exit correctly")
        output = [i for i in p.stdout]
        p.stderr.close()
        p.stdout.close()
        pid, pgid = [int(i.strip()) for i_out in output for i in i_out.split()]
        if platform.system() != "Windows":
            # There is no way of testing this on windows with the current python
            # modules subprocess and os
            self.assertEqual(p.pid, pgid)


if __name__ == '__main__':
    unittest.main(verbosity=2)
