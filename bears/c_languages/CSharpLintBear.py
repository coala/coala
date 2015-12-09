import re

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


class CSharpLintBear(LocalBear, Lint):
    executable = 'mcs'
    output_regex = re.compile(
        r'(?P<filename>.+\.cs)\((?P<line>\d+),(?P<col>\d+)\): '
        r'(?P<severity>error|warning) (?P<severity_code>\w+): (?P<message>.+)'
    )
    use_stderr = True
    severity_map = {
        "warning": RESULT_SEVERITY.NORMAL,
        "error": RESULT_SEVERITY.MAJOR}

    def run(self, filename, file):
        '''
        Checks the code with `mcs` on each file separately.
        '''
        return self.lint(filename)
