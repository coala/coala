import unittest
from queue import Queue

from coalib.settings.Section import Section
from coalib.results.Result import Result, RESULT_SEVERITY
from bears.tests.LocalBearTestHelper import LocalBearTestHelper
from bears.general.LineCountBear import LineCountBear


class LineCountBearTest(LocalBearTestHelper):

    def setUp(self):
        self.uut = LineCountBear(Section("name"), Queue())

    def test_run(self):
        self.assertLinesYieldResult(
            self.uut,
            ["1", "2", "3"],
            Result.from_values(
                "LineCountBear",
                "This file has {count} lines.".format(count=3),
                severity=RESULT_SEVERITY.INFO,
                file="default"))
        self.assertLinesYieldResult(
            self.uut,
            [],
            Result.from_values(
                "LineCountBear",
                "This file has {count} lines.".format(count=0),
                severity=RESULT_SEVERITY.INFO,
                file="default"))


if __name__ == '__main__':
    unittest.main(verbosity=2)
