import os
import subprocess
import sys
from queue import Queue

sys.path.insert(0, ".")
import unittest
from coalib.settings.Setting import Setting
from bears.tests.LocalBearTestHelper import LocalBearTestHelper
from bears.linters.JSHintBear import JSHintBear
from coalib.settings.Section import Section


class JSHintBearTest(LocalBearTestHelper):
    def setUp(self):
        self.section = Section("test section")
        self.uut = JSHintBear(self.section, Queue())
        self.test_file1 = os.path.join(os.path.dirname(__file__),
                                       "test_files",
                                       "jshint_test1.js")
        self.test_file2 = os.path.join(os.path.dirname(__file__),
                                       "test_files",
                                       "jshint_test2.js")
        self.conf_file = os.path.join(os.path.dirname(__file__),
                                      "test_files",
                                      "jshint_config.js")

    def test_run(self):
        # Test a file with errors and warnings
        self.assertLinesInvalid(
            self.uut,
            [],
            self.test_file2)

        # Test a file with a warning which can be changed using a config
        self.assertLinesInvalid(
            self.uut,
            [],
            self.test_file1)

        # Test if warning disappears
        self.section.append(Setting("jshint_config", self.conf_file))
        self.assertLinesValid(
            self.uut,
            [],
            self.test_file1)


def skip_test():
    try:
        subprocess.Popen(['jshint', '--version'],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
        return False
    except OSError:
        return "JSHint is not installed."


if __name__ == '__main__':
    unittest.main(verbosity=2)
