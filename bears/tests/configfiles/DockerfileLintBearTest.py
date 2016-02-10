import os
from queue import Queue
from shutil import which
from unittest.case import skipIf

from bears.configfiles.DockerfileLintBear import DockerfileLintBear
from bears.tests.LocalBearTestHelper import LocalBearTestHelper
from coalib.settings.Section import Section


@skipIf(which('dockerfile_lint') is None, 'dockerfile_lint is not installed')
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
