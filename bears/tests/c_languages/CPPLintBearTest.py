import os
from queue import Queue
from shutil import which
from unittest.case import skipIf

import unittest
from bears.tests.LocalBearTestHelper import LocalBearTestHelper
from bears.c_languages.CPPLintBear import CPPLintBear
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


@skipIf(which('cpplint') is None, 'cpplint is not installed')
class CPPLintBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section("test section")
        self.uut = CPPLintBear(self.section, Queue())
        self.test_file = os.path.join(os.path.dirname(__file__),
                                      "test_files",
                                      "cpplint_bear_test.cpp")

    def test_run(self):
        # Should yield missing copyright line
        self.assertLinesInvalid(self.uut, [], self.test_file)

        # Let's ignore legal issues
        self.section.append(Setting("cpplint_ignore", "legal"))
        self.assertLinesValid(self.uut, [], self.test_file)

    def test_line_length(self):
        self.section.append(Setting("cpplint_ignore", "legal"))
        self.section.append(Setting("max_line_length", "13"))
        self.assertLinesInvalid(self.uut, [], self.test_file)


if __name__ == '__main__':
    unittest.main(verbosity=2)
