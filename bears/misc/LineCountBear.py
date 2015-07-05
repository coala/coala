from coalib.bears.LocalBear import LocalBear
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.results.Result import Result
from coalib.misc.i18n import _


class LineCountBear(LocalBear):
    def run(self, filename, file, *args):
        '''
        Counts the lines of each file.
        '''
        yield Result(
            origin=self,
            message=_("This file has {count} lines.").format(count=len(file)),
            severity=RESULT_SEVERITY.INFO,
            file=filename)
