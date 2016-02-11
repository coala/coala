from queue import Queue

from bears.tests.LocalBearTestHelper import LocalBearTestHelper
from bears.js.JSONFormatBear import JSONFormatBear
from coalib.settings.Section import Section, Setting


class JSONFormatBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section('name')
        self.uut = JSONFormatBear(self.section, Queue())

    def test_valid(self):
        self.check_validity(self.uut, ['{',
                                       '    "a": 5,',
                                       '    "b": 5',
                                       '}'])
        self.check_validity(self.uut, ['{',
                                       '    "b": 5,',
                                       '    "a": 5',
                                       '}'])

    def test_invalid(self):
        self.check_validity(self.uut, [""], valid=False)
        self.check_validity(self.uut, ["random stuff"], valid=False)
        self.check_validity(self.uut, ['{"a":5,"b":5}'], valid=False)

    def test_sorting(self):
        self.section.append(Setting("json_sort", "true"))
        self.check_validity(self.uut, ['{',
                                       '    "b": 5,',
                                       '    "a": 5',
                                       '}'], valid=False)

    def test_indent(self):
        test_code = ['{', '   "b": 5,', '   "a": 5', '}']
        self.check_validity(self.uut, test_code, valid=False)

        self.section.append(Setting("tab_width", "3"))
        self.check_validity(self.uut, test_code)
