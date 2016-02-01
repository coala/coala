import re
from os.path import dirname, abspath, join

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


class CheckstyleBear(LocalBear, Lint):
    executable = 'java'
    google_checks = join(dirname(abspath(__file__)), 'google_checks.xml')
    output_regex = re.compile(
        r'\[(?P<severity>WARN|INFO)\]\s*'
        r'(?P<file_name>.+?):(?P<line>\d+)(:(?P<col>\d+))?:\s*'
        r'(?P<message>.*?)\s*\[(?P<origin>[a-zA-Z]+?)\]')
    severity_map = {
        "INFO": RESULT_SEVERITY.INFO,
        "WARN": RESULT_SEVERITY.NORMAL}

    def run(self, filename, file):
        '''
        Checks the code using `checkstyle`.
        '''
        self.arguments = '-jar checkstyle-6.15-all.jar -c ' + self.google_checks
        return self.lint(filename)
