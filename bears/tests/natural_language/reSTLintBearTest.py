from queue import Queue

from bears.natural_language.reSTLintBear import reSTLintBear
from bears.tests.LocalBearTestHelper import LocalBearTestHelper
from coalib.settings.Section import Section


class reSTLintBearTest(LocalBearTestHelper):

    def setUp(self):
        self.uut = reSTLintBear(Section('name'), Queue())

    def test_valid(self):
        self.assertLinesValid(self.uut, ["test\n====\n"])

    def test_invalid(self):
        self.assertLinesInvalid(self.uut, ["test\n==\n"])
