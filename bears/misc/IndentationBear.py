import re

from coalib.bears.LocalBear import LocalBear
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.results.Result import Result
from coalib.results.Diff import Diff


class MatlabIndentationBear(LocalBear):
    def run(self, filename, file, indentation: int=4):
        indent, nextindent = 0, 0
        for line_nr, line in enumerate(file, start=1):
            indent = nextindent
            indent, nextindent = self.get_indent(line, indent, nextindent)
            stripped = line.lstrip()
            new_line = indent*indentation*' ' + stripped
            if stripped and new_line != line:
                diff = Diff()
                diff.change_line(line_nr, line, new_line)
                yield Result.from_values(
                    self,
                    'Indentation is wrong.',
                    severity=RESULT_SEVERITY.INFO,
                    file=filename,
                    line=line_nr,
                    diffs={filename: diff})

    @staticmethod
    def get_indent(line, indent, nextindent):
        ctrlstart = r'\s*(function|if|while|for|switch)'
        ctrlcont = r'\s*(elseif|else|case|catch|otherwise)'
        ctrlend = r'\s*(end|endfunction|endif|endwhile|endfor|endswitch)'
        if re.match(ctrlstart, line) is not None:
            return indent, nextindent+1
        elif re.match(ctrlcont, line) is not None:
            return indent-1, nextindent
        elif re.match(ctrlend, line) is not None:
            return indent-1, nextindent-1
        else:
            return indent, indent
