from queue import Queue
import sys
import os

sys.path.insert(0, ".")
import unittest
from coalib.settings.Setting import Setting
from bears.tests.LocalBearTestHelper import LocalBearTestHelper
from bears.linters.PyLintBear import PyLintBear
from coalib.settings.Section import Section


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

        self.section.append(Setting("pylint_disable", "E0211"))
        self.assertLinesInvalid(
            self.uut,
            [],
            self.test_file)

        self.section.append(Setting("pylint_disable", "E0211,W0611,C0111"))
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
