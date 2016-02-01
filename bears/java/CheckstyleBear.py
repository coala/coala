import re

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


class CheckstyleBear(LocalBear, Lint):
    executable = 'java'
    arguments = '-jar checkstyle-6.15-all.jar -c google_checks.xml'
    output_regex = re.compile(
        r'\[(?P<severity>WARN|INFO)\]\s*'
        r'(?P<file_name>.+?):(?P<line>\d+)(:(?P<col>\d+))?:\s*'
        r'(?P<message>.*)')
    severity_map = {
        "INFO": RESULT_SEVERITY.INFO,
        "WARN": RESULT_SEVERITY.NORMAL}

    def run(self, filename, file):
        '''
        Checks the code with `checkstyle`.
        '''
        return self.lint(filename)
