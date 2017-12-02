from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


class HiddenBear(LocalBear):

    LANGUAGES = {'all'}

    def run(self, filename, file):
        """
        Is hidden from coala until -d is used.
        """
        yield Result.from_values(
            origin=self,
            message='-d flag works!',
            severity=RESULT_SEVERITY.INFO,
            file=filename)
