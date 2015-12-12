import os
import subprocess
import sys
from queue import Queue

sys.path.insert(0, ".")
import unittest
from bears.tests.LocalBearTestHelper import LocalBearTestHelper
from bears.linters.RubyLintBear import RubyLintBear
from coalib.settings.Section import Section


class RubyLintBearTest(LocalBearTestHelper):
    def setUp(self):
        self.section = Section("test section")
        self.uut = RubyLintBear(self.section, Queue())
        self.test_file1 = os.path.join(os.path.dirname(__file__),
                                       "test_files",
                                       "rubylint_test1.rb")
        self.test_file2 = os.path.join(os.path.dirname(__file__),
                                       "test_files",
                                       "rubylint_test2.rb")

    def test_run(self):
        # Test a file with no issues
        self.assertLinesValid(self.uut, [], self.test_file1)

        # Test a file with issues
        self.assertLinesInvalid(self.uut, [], self.test_file2)


def skip_test():
    try:
        subprocess.Popen(['ruby', '--version'],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
        return False
    except OSError:
        return "Ruby is not installed."


if __name__ == '__main__':
    unittest.main(verbosity=2)
