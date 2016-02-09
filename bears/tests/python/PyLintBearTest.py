import os
import unittest
from queue import Queue
from shutil import which
from unittest.case import skipIf

from coalib.settings.Setting import Setting
from bears.tests.LocalBearTestHelper import LocalBearTestHelper
from bears.python.PyLintBear import PyLintBear
from coalib.settings.Section import Section


@skipIf(which('pylint') is None, 'PyLint is not installed')
class PyLintBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section("test section")
        self.uut = PyLintBear(self.section, Queue())
        self.test_file = os.path.join(os.path.dirname(__file__),
                                      "test_files",
                                      "pylint_test.py")

    def test_run(self):
        self.section.append(Setting("pylint_disable", ""))
        self.assertLinesInvalid(
            self.uut,
            [],  # Doesn't matter, pylint will parse the file
            self.test_file)

        # This is a special case because there's only one result yielded.
        # This was a bug once where the last result got ignored.
        self.section.append(Setting("pylint_disable", "E0211,W0611,C0111"))
        self.assertLinesInvalid(
            self.uut,
            [],
            self.test_file)

        self.section.append(
            Setting("pylint_disable", "E0211,W0611,C0111,W0311"))
        self.assertLinesValid(
            self.uut,
            [],
            self.test_file)

        self.section.append(Setting("pylint_disable", "all"))
        self.assertLinesValid(
            self.uut,
            [],
            self.test_file)

        self.section.append(Setting("pylint_enable", "C0111"))
        self.assertLinesInvalid(
            self.uut,
            [],
            self.test_file)

        self.section.append(Setting("pylint_cli_options", "--disable=all"))
        self.assertLinesValid(
            self.uut,
            [],
            self.test_file)


if __name__ == '__main__':
    unittest.main(verbosity=2)
