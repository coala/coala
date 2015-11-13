from queue import Queue
import sys

sys.path.insert(0, ".")
import unittest
from bears.tests.LocalBearTestHelper import LocalBearTestHelper
from bears.misc.BashSemicolonBear import BashSemicolonBear
from coalib.settings.Section import Section


class BashSemicolonBearTest(LocalBearTestHelper):
    def setUp(self):
        self.uut = BashSemicolonBear(Section("name"), Queue())

    def test_valid(self):
        self.assertLineValid(self.uut, "")
        self.assertLineValid(self.uut, "echo test")
        self.assertLineValid(self.uut, "echo test; echo test2")
        self.assertLineValid(self.uut, " 2) dep_versions=( \"3.5.0\" );;")
        self.assertLineValid(self.uut, " 2) dep_versions=( \"3.5.0\" ) ;;")
        self.assertLineValid(self.uut, "find -type f -exec cat {} \\;")
        self.assertLineValid(self.uut, "echo test  # allowed in comment ;")

    def test_invalid(self):
        self.assertLineInvalid(self.uut, ";")
        self.assertLineInvalid(self.uut, "   ;")
        self.assertLineInvalid(self.uut, "  ;  ")
        self.assertLineInvalid(self.uut, "echo test;")
        self.assertLineInvalid(self.uut, "echo test ; # with comment")
        self.assertLineInvalid(self.uut, "echo test;  ")
        self.assertLineInvalid(self.uut, "echo test  ; ")
        self.assertLineInvalid(self.uut, "echo test; echo test2;")


if __name__ == '__main__':
    unittest.main(verbosity=2)
