import os
from queue import Queue
from shutil import which
from unittest.case import skipIf

from bears.natural_language.ProseLintBear import ProseLintBear
from bears.tests.LocalBearTestHelper import LocalBearTestHelper
from coalib.settings.Section import Section


@skipIf(which('proselint') is None, 'ProseLint is not installed')
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
