from queue import Queue
import sys
import unittest
import subprocess


sys.path.insert(0, ".")
from bears.tests.LocalBearTestHelper import LocalBearTestHelper
from bears.linters.IndentBear import IndentBear
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


class IndentBearTest(LocalBearTestHelper):
    def setUp(self):
        self.section = Section('name')
        self.uut = IndentBear(self.section, Queue())

    def test_valid(self):
        self.assertLinesValid(self.uut, ["int main()\n",
                                         "{\n",
                                         "    return 0;\n",
                                         "}\n"])

    def test_valid_gnu(self):
        self.section.append(Setting("indent_cli_options", "-gnu"))
        self.assertLinesValid(self.uut, ["int\n",
                                         "main ()\n",
                                         "{\n",
                                         "  return 0;\n",
                                         "}\n"])

    def test_invalid(self):
        self.assertLinesInvalid(self.uut, ["int main() {\n",
                                           "  return 0;\n",
                                           "}\n"])


def skip_test():
    try:
        subprocess.Popen([IndentBear.BINARY, '--version'],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
        return False
    except OSError:
        return "indent is not installed."


if __name__ == '__main__':
    unittest.main(verbosity=2)
