from queue import Queue

from bears.tests.BearTestHelper import generate_skip_decorator
from bears.tests.LocalBearTestHelper import LocalBearTestHelper
from bears.c_languages.IndentBear import IndentBear
from coalib.settings.Section import Section


@generate_skip_decorator(IndentBear)
class CorrectionBasedBearTest(LocalBearTestHelper):
    """
    This test only covers corner cases. The basic functionality is tested in
    a more intuitive way in the IndentBearTest.
    """

    def setUp(self):
        self.section = Section('')
        self.queue = Queue()
        self.uut = IndentBear(self.section, self.queue)

    def test_errors(self):
        old_binary, self.uut.executable = self.uut.executable, "invalid_"
        "stuff_here"

        self.uut.execute(filename='', file=[])
        self.queue.get()
        self.assertRegex(str(self.queue.get()), r'\[WARNING\] .*')

        self.uut.executable = old_binary
