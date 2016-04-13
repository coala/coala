from coalib.bears.GlobalBear import GlobalBear
from coalib.results.Result import Result


class GlobalTestBear(GlobalBear):  # pragma: no cover

    def run(self, required_arg: bool):
        for filename in self.file_dict:
            return [Result.from_values("GlobalTestBear", "test msg", filename)]
