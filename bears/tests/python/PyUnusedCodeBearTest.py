from queue import Queue

from bears.tests.LocalBearTestHelper import LocalBearTestHelper
from bears.python.PyUnusedCodeBear import PyUnusedCodeBear
from coalib.settings.Section import Section


class PyUnusedCodeBearTest(LocalBearTestHelper):

    def setUp(self):
        self.uut = PyUnusedCodeBear(Section('name'), Queue())

    def test_valid(self):
        self.check_validity(self.uut, ["import sys; sys.do()"])
        self.check_validity(self.uut, ["a = 2; print(a)"])

    def test_invalid(self):
        self.check_validity(self.uut, ["import os"], valid=False)
        self.check_validity(self.uut, ["pass"], valid=False)
