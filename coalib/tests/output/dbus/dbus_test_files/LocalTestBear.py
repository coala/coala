from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result


class LocalTestBear(LocalBear):  # pragma: no cover
    def run(self, filename, file):
        return [Result("LocalTestBear", "test msg")]
