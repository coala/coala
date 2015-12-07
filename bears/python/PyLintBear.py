import sys
import re

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear
from coalib.settings.Setting import typed_list
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


# We omit this case in our tests for technical reasons
if sys.version_info < (3, 3):  # pragma: no cover
    raise ImportError("PyLint does not support python3 < 3.3")


class PyLintBear(LocalBear, Lint):
    executable = 'pylint'
    arguments = ('--reports=n --persistent=n --msg-template='
                 '"{line}.{column}|{C}: {msg_id} - {msg}"')
    output_regex = re.compile(r'(?P<line>\d+)\.(?P<column>\d+)'
                    r'\|(?P<severity>[WFECRI]): (?P<message>.*)')
    severity_map = {
        "F": RESULT_SEVERITY.MAJOR,
        "E": RESULT_SEVERITY.MAJOR,
        "W": RESULT_SEVERITY.NORMAL,
        "C": RESULT_SEVERITY.INFO,
        "R": RESULT_SEVERITY.INFO,
        "I": RESULT_SEVERITY.INFO}

    def run(self,
            filename,
            file,
            pylint_disable: typed_list(str)=("fixme"),
            pylint_enable: typed_list(str)=None,
            pylint_cli_options: str=""):
        '''
        Checks the code with pylint. This will run pylint over each file
        separately.

        :param pylint_disable:     Disable the message, report, category or
                                   checker with the given id(s).
        :param pylint_enable:      Enable the message, report, category or
                                   checker with the given id(s).
        :param pylint_cli_options: Any command line options you wish to be
                                   passed to pylint.
        '''
        if pylint_disable:
            self.arguments += " --disable=" + ",".join(pylint_disable)
        if pylint_enable:
            self.arguments += " --enable=" + ",".join(pylint_enable)
        if pylint_cli_options:
            self.arguments += " " + pylint_cli_options

        return self.lint(filename)
