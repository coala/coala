import os
import unittest
from queue import Queue
from shutil import which
from unittest.case import skipIf

from bears.tests.LocalBearTestHelper import LocalBearTestHelper
from bears.c_languages.CSharpLintBear import CSharpLintBear
from coalib.settings.Section import Section


@skipIf(which('mcs') is None, 'mono mcs is not installed')
class CSharpLintBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section("test section")
        self.uut = CSharpLintBear(self.section, Queue())
        self.test_file1 = os.path.join(os.path.dirname(__file__),
                                       "test_files",
                                       "csharplint_test1.cs")
        self.test_file2 = os.path.join(os.path.dirname(__file__),
                                       "test_files",
                                       "csharplint_test2.cs")

    def test_run(self):
        # Test a file with no issues
        self.assertLinesValid(self.uut, [], self.test_file1)

        # Test a file with issues
        self.assertLinesInvalid(self.uut, [], self.test_file2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
