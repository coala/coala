import re

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


class PHPLintBear(LocalBear, Lint):
    executable = 'php'
    arguments = '-l -n -d display_errors=On -d log_errors=Off'
    output_regex = re.compile(
        r'(?P<severity>\S+) error: '
        r'(?P<message>.*) in (?P<file_name>.*) on line (?P<line>\d+)')
    severity_map = {
        "Parse": RESULT_SEVERITY.MAJOR,
        "Fatal": RESULT_SEVERITY.MAJOR}

    def run(self, filename, file):
        '''
        Checks the code with `php -l`. This runs it on each file separately.
        '''
        return self.lint(filename)
