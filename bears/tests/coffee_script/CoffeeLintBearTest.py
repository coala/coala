import os
import unittest
from queue import Queue
from shutil import which
from unittest.case import skipIf

from bears.tests.LocalBearTestHelper import LocalBearTestHelper
from bears.coffee_script.CoffeeLintBear import CoffeeLintBear
from coalib.settings.Section import Section


@skipIf(which('coffeelint') is None, 'coffeelint is not installed')
class CoffeeLintBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section("test section")
        self.uut = CoffeeLintBear(self.section, Queue())

    @staticmethod
    def get_test_filename(basename):
        return os.path.join(os.path.dirname(__file__),
                            "test_files",
                            basename + ".coffee")

    def test_good(self):
        good_file = self.get_test_filename("good")
        self.assertLinesValid(self.uut, [], good_file)

    def test_warn(self):
        warn_file = self.get_test_filename("warning")
        self.assertLinesInvalid(self.uut, [], warn_file)

    def test_err(self):
        err_file = self.get_test_filename("error")
        self.assertLinesInvalid(self.uut, [], err_file)

    def test_invalid(self):
        # CoffeeLint will generate an invalid CSV on this one!
        invalid_file = self.get_test_filename("invalid")
        self.assertLinesInvalid(self.uut, [], invalid_file)


if __name__ == '__main__':
    unittest.main(verbosity=2)
