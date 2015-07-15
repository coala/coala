from subprocess import Popen, PIPE
import sys

from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result, RESULT_SEVERITY
from coalib.settings.Setting import typed_list
from coalib.misc.Shell import escape_path_argument


# We omit this case in our tests for technical reasons
if sys.version_info < (3, 3):  # pragma: no cover
    raise ImportError("PyLint does not support python3 < 3.3")


class PyLintBear(LocalBear):
    def parse_result(self, file, pylint_line):
        parts = pylint_line.split("|", maxsplit=2)

        line_nr = int(parts[0])
        severity = parts[1]
        if severity == "warning":
            severity = RESULT_SEVERITY.NORMAL
        elif severity in ["error", "fatal"]:
            severity = RESULT_SEVERITY.MAJOR
        else:  # convention and refactor
            severity = RESULT_SEVERITY.INFO

        message = parts[2]

        return Result(self.__class__.__name__,
                      message,
                      file,
                      severity,
                      line_nr)

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
        command = ('pylint -r n --msg-template="{line}|{category}|'
                   '{msg}. ({msg_id}, {symbol}, {obj})" '
                   + escape_path_argument(filename))
        if pylint_disable:
            command += " --disable=" + ",".join(pylint_disable)
        if pylint_enable:
            command += " --enable=" + ",".join(pylint_enable)
        if pylint_cli_options:
            command += " " + pylint_cli_options

        process = Popen(command,
                        shell=True,
                        stdout=PIPE,
                        stderr=PIPE,
                        universal_newlines=True)
        process.wait()
        current_lines = ""
        for line in process.stdout.readlines():
            if line.startswith("***"):
                continue

            if current_lines != "" and line.split("|", 1)[0].isdigit():
                yield self.parse_result(filename, current_lines)
                current_lines = ""

            current_lines += line

        process.stdout.close()
        process.stderr.close()
