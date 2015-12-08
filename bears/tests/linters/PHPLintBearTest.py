import os
import subprocess
import sys
from queue import Queue

sys.path.insert(0, ".")
import unittest
from bears.tests.LocalBearTestHelper import LocalBearTestHelper
from bears.linters.PHPLintBear import PHPLintBear
from coalib.settings.Section import Section


class PHPLintBearTest(LocalBearTestHelper):
    def setUp(self):
        self.section = Section("test section")
        self.uut = PHPLintBear(self.section, Queue())
        self.test_file1 = os.path.join(os.path.dirname(__file__),
                                       "test_files",
                                       "phplint_test1.php")
        self.test_file2 = os.path.join(os.path.dirname(__file__),
                                       "test_files",
                                       "phplint_test2.php")

    def test_run(self):
        # Test a file with errors and warnings
        self.assertLinesInvalid(
            self.uut,
            [],
            self.test_file1)

        # Test a file without any issues
        self.assertLinesValid(
            self.uut,
            [],
            self.test_file2)


def skip_test():
    try:
        subprocess.Popen(['php', '--version'],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
        return False
    except OSError:
        return "PHP is not installed."


if __name__ == '__main__':
    unittest.main(verbosity=2)
