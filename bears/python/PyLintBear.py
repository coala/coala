import os
import re

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear
from coalib.misc.Shell import escape_path_argument
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.settings.Setting import typed_list


class PyLintBear(LocalBear, Lint):
    executable = 'pylint'
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
            pylint_disable: typed_list(str)=None,
            pylint_enable: typed_list(str)=None,
            pylint_cli_options: str="",
            pylint_rcfile: str=""):
        '''
        Checks the code with pylint. This will run pylint over each file
        separately.

        :param pylint_disable:     Disable the message, report, category or
                                   checker with the given id(s).
        :param pylint_enable:      Enable the message, report, category or
                                   checker with the given id(s).
        :param pylint_cli_options: Any command line options you wish to be
                                   passed to pylint.
        :param pylint_rcfile:      The rcfile for PyLint.
        '''
        self.arguments = ('--reports=n --persistent=n '
                          '--msg-template="{{line}}.{{column}}|{{C}}: '
                          '{{msg_id}} - {{msg}}"')
        if pylint_disable:
            self.arguments += " --disable=" + ",".join(pylint_disable)
        if pylint_enable:
            self.arguments += " --enable=" + ",".join(pylint_enable)
        if pylint_cli_options:
            self.arguments += " " + pylint_cli_options
        if pylint_rcfile:
            self.arguments += " --rcfile=" + escape_path_argument(pylint_rcfile)
        else:
            self.arguments += " --rcfile=" + os.devnull
        self.arguments += " {filename}"

        return self.lint(filename)
