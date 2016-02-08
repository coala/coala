import os
import sys
from queue import Queue
from shutil import which
from unittest.case import skipIf

sys.path.insert(0, ".")
import unittest
from coalib.settings.Setting import Setting
from bears.tests.LocalBearTestHelper import LocalBearTestHelper
from bears.go.GoLintBear import GoLintBear
from coalib.settings.Section import Section


@skipIf(which('golint') is None, 'golint is not installed')
class GoLintBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section("Test Section")
        self.uut = GoLintBear(self.section, Queue())
        self.good_file = os.path.join(os.path.dirname(__file__),
                                      "test_files",
                                      "golint_good.go")
        self.bad_file = os.path.join(os.path.dirname(__file__),
                                     "test_files",
                                     "golint_bad.go")

    def test_run(self):
        self.assertLinesValid(self.uut, [], self.good_file)
        self.assertLinesInvalid(self.uut, [], self.bad_file)
        self.section.append(Setting("golint_cli_options",
                                    "-min_confidence=0.8"))
        self.assertLinesInvalid(self.uut, [], self.bad_file)

if __name__ == '__main__':
    unittest.main(verbosity=2)
