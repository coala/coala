import os
from queue import Queue
from shutil import which
from unittest.case import skipIf
import unittest

from bears.tests.LocalBearTestHelper import LocalBearTestHelper
from bears.go.GoVetBear import GoVetBear
from coalib.settings.Section import Section


@skipIf(which('go') is None, 'go is not installed')
class GoVetBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section("test section")
        self.uut = GoVetBear(self.section, Queue())
        self.good_file = os.path.join(os.path.dirname(__file__),
                                      "test_files",
                                      "vet_good.go")
        self.bad_file = os.path.join(os.path.dirname(__file__),
                                     "test_files",
                                     "vet_bad.go")

    def test_run(self):
        self.assertLinesValid(self.uut, [], self.good_file)
        self.assertLinesInvalid(self.uut, [], self.bad_file)


if __name__ == '__main__':
    unittest.main(verbosity=2)
