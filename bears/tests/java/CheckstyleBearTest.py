import os
from queue import Queue
from shutil import which
from unittest.case import skipIf

from bears.java.CheckstyleBear import CheckstyleBear
from bears.tests.LocalBearTestHelper import LocalBearTestHelper
from coalib.settings.Section import Section


@skipIf(which('java') is None, 'java is not installed')
class CheckstyleBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section("test section")
        self.uut = CheckstyleBear(self.section, Queue())
        self.good_file = os.path.join(os.path.dirname(__file__),
                                      "test_files",
                                      "CheckstyleGood.java")
        self.bad_file = os.path.join(os.path.dirname(__file__),
                                     "test_files",
                                     "CheckstyleBad.java")

    def test_run(self):
        self.check_validity(self.uut, [], self.good_file)
        self.check_validity(self.uut, [], self.bad_file, valid=False)
