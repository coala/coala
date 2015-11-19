import sys
import unittest
from queue import Queue

sys.path.insert(0, ".")
from bears.tests.LocalBearTestHelper import LocalBearTestHelper
from bears.python.PEP8Bear import PEP8Bear
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


class PEP8BearTest(LocalBearTestHelper):
    def setUp(self):
        self.section = Section('name')
        self.uut = PEP8Bear(self.section, Queue())

    def test_valid(self):
        self.assertLinesValid(self.uut, ["import sys"])
        self.assertLinesValid(self.uut, ["a = 1 + 1"])

    def test_disable_warnings(self):
        test_code = ['def func():\n',
                     '    pass\n',
                     'def func2():\n',
                     '    pass\n']
        self.assertLinesInvalid(self.uut, test_code)

        self.section.append(Setting('pep_ignore', 'E302'))
        self.assertLinesValid(self.uut, test_code)

    def test_invalid(self):
        self.assertLinesInvalid(self.uut, [""])
        self.assertLinesInvalid(self.uut, ["a=1+1"])


if __name__ == '__main__':
    unittest.main(verbosity=2)
