import time

from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result


class ProcessingLocalTestBear(LocalBear):  # pragma: no cover

    def run(self, filename, file):
        # we need to test that the SectionExecutor holds back the global
        # results until processing of all local ones is finished
        time.sleep(0.05)
        return [Result('LocalTestBear', 'test msg')]
