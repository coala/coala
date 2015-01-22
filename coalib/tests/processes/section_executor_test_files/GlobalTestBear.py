from coalib.bears.GlobalBear import GlobalBear
from coalib.bears.results.Result import Result


class GlobalTestBear(GlobalBear):  # pragma: no cover
    def run_bear(self):
        for filename in self.file_dict:
            return [Result("GlobalTestBear", "test message", filename)]
