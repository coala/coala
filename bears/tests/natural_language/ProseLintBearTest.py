import os
import subprocess
import sys
from queue import Queue

sys.path.insert(0, ".")
import unittest
from bears.tests.LocalBearTestHelper import LocalBearTestHelper
from bears.natural_language.ProseLintBear import ProseLintBear
from coalib.settings.Section import Section


class ProseLintBearTest(LocalBearTestHelper):
    def setUp(self):
        self.section = Section("test section")
        self.uut = ProseLintBear(self.section, Queue())
        self.test_file1 = os.path.join(os.path.dirname(__file__),
                                       "test_files",
                                       "proselint_test1.md")
        self.test_file2 = os.path.join(os.path.dirname(__file__),
                                       "test_files",
                                       "proselint_test2.md")

    def test_run(self):
        # Test a file with no issues
        self.assertLinesValid(self.uut, [], self.test_file1)

        # Test a file with issues
        self.assertLinesInvalid(self.uut, [], self.test_file2)


def skip_test():
    try:
        subprocess.Popen(['proselint', '--version'],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
        return False
    except OSError:
        return "ProseLint is not installed."


if __name__ == '__main__':
    unittest.main(verbosity=2)
