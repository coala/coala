import re
import shlex

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


class JSHintBear(LocalBear, Lint):
    executable = 'jshint'
    output_regex = re.compile(
        r'.+?: line (?P<line>\d+), col (?P<col>\d+), '
        r'(?P<message>.+) \((?P<severity>\S)\d+\)')
    severity_map = {
        "E": RESULT_SEVERITY.MAJOR,
        "W": RESULT_SEVERITY.NORMAL,
        "I": RESULT_SEVERITY.NORMAL}

    def run(self,
            filename,
            file,
            jshint_config: str=""):
        '''
        Checks the code with jshint. This will run jshint over each file
        separately.

        :param jshint_config: The location of the jshintrc config file.
        '''
        self.arguments = '--verbose {filename}'
        if jshint_config:
            self.arguments += (" --config "
                               + shlex.quote(jshint_config))

        return self.lint(filename)
