import re

from bears.linters.CorrectionBasedBear import CorrectionBasedBear
from coalib.results.Result import Result


class AlexBear(CorrectionBasedBear):
    BINARY = 'alex'
    REGEX = (r'^\s+(?P<line>\d+):(?P<col>\d+)\-(?P<toline>\d+):(?P<tocol>\d+)'
             r'\s+(?:(?P<warning>warning)) (?P<message>.+)')

    def run(self, filename, file):
        output, errors = self._run_process(file, '')
        self._print_errors(errors)

        for line in output:
            match = re.match(self.REGEX, line)
            if match:
                groupdict = match.groupdict()
                yield Result.from_values(self,
                                         groupdict['message'],
                                         filename,
                                         line=int(groupdict['line']),
                                         column=int(groupdict['col']),
                                         end_line=int(groupdict['toline']),
                                         end_column=int(groupdict['tocol']))
