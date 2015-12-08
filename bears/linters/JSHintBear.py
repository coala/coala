import re

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.misc.Shell import escape_path_argument


class JSHintBear(LocalBear, Lint):
    executable = 'jshint'
    arguments = '--verbose'
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
        if jshint_config:
            self.arguments += (" --config "
                               + escape_path_argument(jshint_config))

        return self.lint(filename)
