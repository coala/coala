from coalib.bears.GlobalBear import GlobalBear
from coalib.results.Result import Result


class ProcessingGlobalTestRawFileBear(GlobalBear):

    USE_RAW_FILES = True

    def run(self):
        for filename in self.file_dict:
            return [Result.from_values('GlobalTestRawBear',
                                       'test message',
                                       filename)]
