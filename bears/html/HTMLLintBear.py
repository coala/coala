import re

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.settings.Setting import typed_list


class HTMLLintBear(LocalBear, Lint):
    executable = 'html_lint.py'
    output_regex = re.compile(
        r'(?P<line>\d+):(?P<column>\d+):\s'
        r'(?P<severity>Error|Warning|Info):\s(?P<message>.+)'
    )
    severity_map = {
        "Info": RESULT_SEVERITY.INFO,
        "Warning": RESULT_SEVERITY.NORMAL,
        "Error": RESULT_SEVERITY.MAJOR
    }

    def run(self,
            filename,
            file,
            htmllint_ignore: typed_list(str)=[]):
        '''
        Checks the code with `html_lint.py` on each file separately.

        :param htmllint_include: List of checkers to ignore.
        '''
        ignore = ','.join(part.strip() for part in htmllint_ignore)
        self.arguments = '--disable=' + ignore
        self.arguments += " {filename}"
        return self.lint(filename)
