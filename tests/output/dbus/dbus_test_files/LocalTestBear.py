from coalib.bears.LocalBear import LocalBear
from coalib.results.HiddenResult import HiddenResult
from coalib.results.Result import Result


class LocalTestBear(LocalBear):  # pragma: no cover

    def run(self, filename, file):
        return [Result("LocalTestBear", "test msg"),
                HiddenResult("LocalTestBear", "hidden msg")]
