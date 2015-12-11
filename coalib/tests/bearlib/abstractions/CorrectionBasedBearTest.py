import subprocess
import sys
import unittest
from queue import Queue

sys.path.insert(0, ".")
from bears.tests.LocalBearTestHelper import LocalBearTestHelper
from bears.c_languages.IndentBear import IndentBear
from coalib.settings.Section import Section


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
        old_binary, self.uut.BINARY = self.uut.BINARY, "invalid_stuff_here"

        self.uut.execute(filename='', file=[])
        self.queue.get()
        self.assertRegex(str(self.queue.get()), r'\[WARNING\] .*')

        self.uut.BINARY = old_binary


def skip_test():
    try:
        subprocess.Popen([IndentBear.BINARY, '--version'],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
        return False
    except OSError:
        return "indent is not installed."


if __name__ == '__main__':
    unittest.main(verbosity=2)
