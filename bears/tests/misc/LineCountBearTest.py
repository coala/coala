from queue import Queue
import sys

sys.path.insert(0, ".")
import unittest
from coalib.settings.Section import Section
from coalib.results.Result import Result, RESULT_SEVERITY
from bears.tests.LocalBearTestHelper import LocalBearTestHelper
from bears.misc.LineCountBear import LineCountBear, _


class SpaceConsistencyBearTest(LocalBearTestHelper):
    def setUp(self):
        self.uut = LineCountBear(Section("name"), Queue())

    def test_run(self):
        self.assertLinesYieldResult(
            self.uut,
            ["1", "2", "3"],
            Result("LineCountBear",
                   _("This file has {count} lines.").format(count=3),
                   severity=RESULT_SEVERITY.INFO,
                   file="default"))
        self.assertLinesYieldResult(
            self.uut,
            [],
            Result("LineCountBear",
                   _("This file has {count} lines.").format(count=0),
                   severity=RESULT_SEVERITY.INFO,
                   file="default"))


if __name__ == '__main__':
    unittest.main(verbosity=2)
