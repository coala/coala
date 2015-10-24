from coalib.bears.GlobalBear import GlobalBear
from coalib.results.Result import Result


class GlobalTestBear(GlobalBear):  # pragma: no cover
    def run(self):
        for filename in self.file_dict:
            return [Result.from_values("GlobalTestBear",
                                       "test message",
                                       filename)]
