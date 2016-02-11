from queue import Queue

from bears.tests.BearTestHelper import generate_skip_decorator
from bears.tests.LocalBearTestHelper import LocalBearTestHelper
from bears.c_languages.IndentBear import IndentBear
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


@generate_skip_decorator(IndentBear)
class IndentBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section('name')
        self.section.append(Setting("use_spaces", "true"))
        self.section.append(Setting("max_line_length", "80"))
        self.uut = IndentBear(self.section, Queue())

    def test_valid(self):
        self.check_validity(self.uut, ["int\n",
                                       "main ()\n",
                                       "{\n",
                                       "    return 0;\n",
                                       "}\n"])

    def test_tab_width(self):
        self.section.append(Setting("tab_width", "2"))
        self.check_validity(self.uut, ["int\n",
                                       "main ()\n",
                                       "{\n",
                                       "  return 0;\n",
                                       "}\n"])

    def test_tabs(self):
        test_code = ["int\n", "main ()\n", "{\n", "\treturn 0;\n", "}\n"]
        self.check_validity(self.uut, test_code, valid=False)

        self.section.append(Setting("use_spaces", "nope"))
        self.check_validity(self.uut, test_code)

    def test_invalid(self):
        self.check_validity(self.uut, ["int main() {\n",
                                       "  return 0;\n",
                                       "}\n"], valid=False)
