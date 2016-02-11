from queue import Queue

from bears.tests.LocalBearTestHelper import LocalBearTestHelper
from bears.python.PyCommentedCodeBear import PyCommentedCodeBear
from coalib.settings.Section import Section


class PyCommentedCodeBearTest(LocalBearTestHelper):

    def setUp(self):
        self.uut = PyCommentedCodeBear(Section('name'), Queue())

    def test_valid(self):
        self.check_validity(self.uut, ["import sys"])
        self.check_validity(self.uut, ["a = 1 + 1"])
        self.check_validity(self.uut, ["# hey man!"])
        self.check_validity(self.uut, ['"""',
                                       'Hey, this is a code sample:',
                                       '>>> import os',
                                       '',
                                       'And when you use it you can simply '
                                       'do: `import os`.',
                                       '"""'])

    def test_invalid(self):
        self.check_validity(self.uut, ["# import os"], valid=False)
        self.check_validity(self.uut, ["# print('comment')"], valid=False)
