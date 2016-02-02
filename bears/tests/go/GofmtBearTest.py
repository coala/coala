import sys
from queue import Queue
from shutil import which
from unittest.case import skipIf

sys.path.insert(0, ".")
import unittest
from bears.tests.LocalBearTestHelper import LocalBearTestHelper
from bears.go.GofmtBear import GofmtBear
from coalib.settings.Section import Section


@skipIf(which('gofmt') is None, 'gofmt is not installed')
class GoVetBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section("test section")
        self.uut = GofmtBear(self.section, Queue())

    def test_run(self):
        self.assertLinesInvalid(self.uut,
                                ['package main',
                                 'func main() {',
                                 '    return 1',
                                 '}'])
        self.assertLinesValid(self.uut,
                              ['package main',
                               '',
                               'func main() {',
                               '\treturn 1',
                               '}'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
