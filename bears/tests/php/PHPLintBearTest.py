import os
import unittest
from queue import Queue
from shutil import which
from unittest.case import skipIf

from bears.tests.LocalBearTestHelper import LocalBearTestHelper
from bears.php.PHPLintBear import PHPLintBear
from coalib.settings.Section import Section


@skipIf(which('php') is None, 'PHP is not installed')
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


if __name__ == '__main__':
    unittest.main(verbosity=2)
