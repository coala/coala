from coalib.bears.LocalBear import LocalBear
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.results.Result import Result


class LineCountBear(LocalBear):
    def run(self, filename, file, *args):
        '''
        Counts the lines of each file.
        '''
        yield Result.from_values(
            origin=self,
            message="This file has {count} lines.".format(count=len(file)),
            severity=RESULT_SEVERITY.INFO,
            file=filename)
