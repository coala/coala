import os
import unittest
from queue import Queue
from shutil import which
from unittest.case import skipIf

from bears.tests.LocalBearTestHelper import LocalBearTestHelper
from bears.natural_language.AlexBear import AlexBear
from coalib.settings.Section import Section


@skipIf(which('alex') is None, 'Alex is not installed')
class AlexBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section("test section")
        self.uut = AlexBear(self.section, Queue())
        self.test_file1 = os.path.join(os.path.dirname(__file__),
                                       "test_files",
                                       "alex_test1.md")
        self.test_file2 = os.path.join(os.path.dirname(__file__),
                                       "test_files",
                                       "alex_test2.md")

    def test_run(self):
        # Test a file with no issues
        self.assertLinesValid(self.uut, [], self.test_file1)

        # Test a file with issues
        self.assertLinesInvalid(self.uut, [], self.test_file2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
