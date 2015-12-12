import re

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


class RubyLintBear(LocalBear, Lint):
    executable = 'ruby'
    arguments = '-wc'
    output_regex = re.compile(
        r'(?P<file_name>.+?):(?P<line>\d+): (?P<message>'
        r'.*?(?P<severity>error|warning)[,:] [^\r\n]+)\r?\n'
        r'(?:^[^\r\n]+\r?\n^(?P<col>.*?)\^)?')
    use_stderr = True
    severity_map = {
        "warning": RESULT_SEVERITY.NORMAL,
        "error": RESULT_SEVERITY.MAJOR}

    def run(self, filename, file):
        '''
        Checks the code with `ruby -wc` on each file separately.
        '''
        return self.lint(filename)
