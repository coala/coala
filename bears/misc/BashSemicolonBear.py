import re

from coalib.results.Result import Result
from coalib.bears.LocalBear import LocalBear
from coalib.misc.i18n import _
from coalib.results.Diff import Diff
from coalib.parsing.StringProcessing import (unescaped_search_for,
                                             unescaped_search_in_between)


class BashSemicolonBear(LocalBear):
    SEMICOLON_OK = re.compile(r'[^;]*(;;|\\;)\s*$')
    SEMICOLON_WARN = re.compile(r'.*\s*;\s*$')

    def run(self,
            filename,
            file):
        '''
        Checks bash code for inappropriate semicolons. Please note the following
        shortcomings:

        - it does not understand multiline comments. (See
          http://www.cyberciti.biz/faq/bash-comment-out-multiple-line-code/)
        - it ignores the double semicolon (;;) because it would need more
          advanced parsing to check if they are in a proper case statement.
        '''
        for line_number, line in enumerate(file, start=1):
            if (
                    not self.SEMICOLON_OK.match(line) and
                    self.SEMICOLON_WARN.match(line)):
                position = line.rfind(';')
                diff = Diff()
                diff.change_line(line_number, line, line[:position] + "\n")
                yield Result.from_values(
                    origin=self,
                    message=_("The line contains an unneeded semicolon."),
                    file=filename,
                    line=line_number,
                    column=position+1,
                    end_line=line_number,
                    end_column=position+2,
                    diffs={filename: diff})
