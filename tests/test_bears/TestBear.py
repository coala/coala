from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result


class TestBear(LocalBear):

    def run(self, file, filename, result: bool=False, exception: bool = False):
        if result:
            yield result

        if exception:
            raise ValueError
