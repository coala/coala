import os
import subprocess
import sys
from queue import Queue

sys.path.insert(0, ".")
import unittest
from bears.tests.LocalBearTestHelper import LocalBearTestHelper
from bears.linters.DockerfileLintBear import DockerfileLintBear
from coalib.settings.Section import Section


class DockerfileLintBearTest(LocalBearTestHelper):
    def setUp(self):
        self.section = Section("test section")
        self.uut = DockerfileLintBear(self.section, Queue())
        self.test_file1 = os.path.join(os.path.dirname(__file__),
                                       "test_files",
                                       "dockerfilelint_test1")
        self.test_file2 = os.path.join(os.path.dirname(__file__),
                                       "test_files",
                                       "dockerfilelint_test2")

    def test_run(self):
        self.assertLinesValid(self.uut, [], self.test_file1)
        self.assertLinesInvalid(self.uut, [], self.test_file2)


def skip_test():
    try:
        subprocess.Popen(['dockerfile_lint', '--version'],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
        return False
    except OSError:
        return "dockerfile-lint is not installed."


if __name__ == '__main__':
    unittest.main(verbosity=2)
