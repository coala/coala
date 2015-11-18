from queue import Queue
import sys
import unittest

sys.path.insert(0, ".")
from bears.tests.LocalBearTestHelper import LocalBearTestHelper
from bears.linters.ClangBear import ClangBear
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting
from coalib.bearlib.parsing.clang.cindex import Index, LibclangError


class ClangBearTest(LocalBearTestHelper):
    def setUp(self):
        self.section = Section('name')
        self.uut = ClangBear(self.section, Queue())

    def test_valid(self):
        self.assertLinesValid(self.uut, ["int main() {}"], filename="test.c")

    def test_disable_warnings(self):
        self.section.append(Setting('clang_cli_options', '-w'))
        self.assertLinesValid(self.uut,
                              ["struct { int f0; } x = { f0 :1 };"],
                              filename="test.c")

    def test_invalid(self):
        # Has no fixit
        self.assertLinesInvalid(self.uut,
                                ["bad things, this is no C code"],
                                filename="test.c")

        # Has a fixit and no range, should use range from fixit
        self.assertLinesInvalid(self.uut,
                                ["struct { int f0; } x = { f0 :1 };"],
                                filename="test.c")

        # Has a fixit and a range
        self.assertLinesInvalid(self.uut,
                                ["int main() {int *b; return b}"],
                                filename="test.c")


def skip_test():
    try:
        Index.create()
        return False
    except LibclangError as error:
        return str(error)


if __name__ == '__main__':
    unittest.main(verbosity=2)
