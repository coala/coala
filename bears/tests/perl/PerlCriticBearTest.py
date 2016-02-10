import os
from queue import Queue
from shutil import which
from unittest.case import skipIf

from bears.perl.PerlCriticBear import PerlCriticBear
from bears.tests.LocalBearTestHelper import LocalBearTestHelper
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


@skipIf(which('perlcritic') is None, 'perlcritic is not installed')
class PerlCriticBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section("Test Section")
        self.uut = PerlCriticBear(self.section, Queue())
        self.good_file = os.path.join(os.path.dirname(__file__),
                                      "test_files",
                                      "perlcritic_good.pl")
        self.bad_file = os.path.join(os.path.dirname(__file__),
                                     "test_files",
                                     "perlcritic_bad.pl")
        self.conf_file = os.path.join(os.path.dirname(__file__),
                                      "test_files",
                                      "perlcritic_config.pl")

    def test_run(self):
        self.assertLinesValid(self.uut, [], self.good_file)
        self.assertLinesInvalid(self.uut, [], self.bad_file)
        self.section.append(Setting("perlcritic_config", self.conf_file))
        self.assertLinesValid(self.uut, [], self.bad_file)
