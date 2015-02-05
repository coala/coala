from coalib.bears.LocalBear import LocalBear
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.results.Result import Result
from coalib.misc.i18n import _


class LineCountBear(LocalBear):
    def run_bear(self, filename, file, *args):
        """
        Counts the lines of each file.
        """
        return [Result(
            self.__class__.__name__,
            _("This file has {count} lines.").format(count=len(file)),
            RESULT_SEVERITY.INFO
        )]
