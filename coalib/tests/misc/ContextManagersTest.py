import unittest
import sys
import subprocess
import os

from coalib.misc.ContextManagers import (suppress_stdout,
                                         retrieve_stdout,
                                         simulate_console_inputs,
                                         subprocess_timeout,
                                         make_temp)
from coalib.processes.Processing import create_process_group


process_group_timeout_test_code = """
import time, subprocess, sys;
p = subprocess.Popen([sys.executable,
                     "-c",
                     "import time; time.sleep(100)"]);
time.sleep(100);
"""


class ContextManagersTest(unittest.TestCase):

    def test_subprocess_timeout(self):
        p = subprocess.Popen([sys.executable,
                              "-c",
                              "import time; time.sleep(0.5);"],
                             stderr=subprocess.PIPE)
        with subprocess_timeout(p, 0.2) as timedout:
            retval = p.wait()
            p.stderr.close()
            self.assertEqual(timedout.value, True)
        self.assertNotEqual(retval, 0)

        p = create_process_group([sys.executable,
                                  "-c",
                                  process_group_timeout_test_code])
        with subprocess_timeout(p, 0.5, kill_pg=True):
            retval = p.wait()
            self.assertEqual(timedout.value, True)
        self.assertNotEqual(retval, 0)

        p = subprocess.Popen([sys.executable,
                              "-c",
                              "import time"])
        with subprocess_timeout(p, 0.5) as timedout:
            retval = p.wait()
            self.assertEqual(timedout.value, False)
        self.assertEqual(retval, 0)

        p = subprocess.Popen([sys.executable,
                              "-c",
                              "import time"])
        with subprocess_timeout(p, 0) as timedout:
            retval = p.wait()
            self.assertEqual(timedout.value, False)
        self.assertEqual(retval, 0)

    def test_suppress_stdout(self):
        def print_func():
            print("func")
            raise NotImplementedError

        def no_print_func():
            with suppress_stdout():
                print("func")
                raise NotImplementedError

        old_stdout = sys.stdout
        sys.stdout = False

        self.assertRaises(AttributeError, print_func)
        self.assertRaises(NotImplementedError, no_print_func)

        sys.stdout = old_stdout

    def test_retrieve_stdout(self):
        with retrieve_stdout() as sio:
            print("test")
            self.assertEqual(sio.getvalue(), "test\n")

    def test_simulate_console_inputs(self):
        with simulate_console_inputs(0, 1, 2) as generator:
            self.assertEqual(input(), 0)
            self.assertEqual(generator.last_input, 0)
            generator.inputs.append(3)
            self.assertEqual(input(), 1)
            self.assertEqual(input(), 2)
            self.assertEqual(input(), 3)
            self.assertEqual(generator.last_input, 3)

        with simulate_console_inputs("test"), self.assertRaises(ValueError):
            self.assertEqual(input(), "test")
            input()

    def test_make_temp(self):
        with make_temp() as f_a:
            self.assertTrue(os.path.isfile(f_a))
            self.assertTrue(os.path.basename(f_a).startswith("tmp"))

        with make_temp(suffix=".orig", prefix="pre") as f_b:
            self.assertTrue(f_b.endswith(".orig"))
            self.assertTrue(os.path.basename(f_b).startswith("pre"))


if __name__ == '__main__':
    unittest.main(verbosity=2)
