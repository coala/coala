from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result
from coalib.results.HiddenResult import HiddenResult


class LocalTestBear(LocalBear):  # pragma: no cover
    def run(self, filename, file):
        return [Result("LocalTestBear", "test msg"),
                HiddenResult("LocalTestBear", "hidden msg")]
