import unittest
from queue import Queue

from bears.tests.LocalBearTestHelper import LocalBearTestHelper
from bears.js.JSONFormatBear import JSONFormatBear
from coalib.settings.Section import Section, Setting


class JSONFormatBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section('name')
        self.uut = JSONFormatBear(self.section, Queue())

    def test_valid(self):
        self.assertLinesValid(self.uut, ['{',
                                         '    "a": 5,',
                                         '    "b": 5',
                                         '}'])
        self.assertLinesValid(self.uut, ['{',
                                         '    "b": 5,',
                                         '    "a": 5',
                                         '}'])

    def test_invalid(self):
        self.assertLinesInvalid(self.uut, [""])
        self.assertLinesInvalid(self.uut, ["random stuff"])
        self.assertLinesInvalid(self.uut, ['{"a":5,"b":5}'])

    def test_sorting(self):
        self.section.append(Setting("json_sort", "true"))
        self.assertLinesInvalid(self.uut, ['{',
                                           '    "b": 5,',
                                           '    "a": 5',
                                           '}'])

    def test_indent(self):
        test_code = ['{', '   "b": 5,', '   "a": 5', '}']
        self.assertLinesInvalid(self.uut, test_code)

        self.section.append(Setting("tab_width", "3"))
        self.assertLinesValid(self.uut, test_code)


if __name__ == '__main__':
    unittest.main(verbosity=2)
