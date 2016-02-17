import re

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


class LatexLintBear(LocalBear, Lint):
    executable = 'chktex'
    output_regex = re.compile(r'(?P<severity>Error|Warning) (?P<num>[0-9]+)'
                              r' in (?P<file_name>\S+) line (?P<line>[0-9]+)'
                              r': (?P<message>.*)')
    severity_map = {'Warning': RESULT_SEVERITY.NORMAL,
                    'Error': RESULT_SEVERITY.MAJOR}
    arguments = "{filename}"

    def run(self, filename, file):
        '''
        Checks the code with `chktex`.
        '''
        return self.lint(filename)
