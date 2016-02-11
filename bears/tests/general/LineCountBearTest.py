from queue import Queue

from bears.general.LineCountBear import LineCountBear
from bears.tests.LocalBearTestHelper import LocalBearTestHelper
from coalib.results.Result import RESULT_SEVERITY, Result
from coalib.settings.Section import Section


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
