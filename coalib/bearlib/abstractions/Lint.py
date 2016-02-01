import subprocess
import tempfile
import re
import sys

from coalib.bearlib.abstractions.CorrectionBasedBear import is_binary_present
from coalib.misc.Shell import escape_path_argument
from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.bears.Bear import Bear


class Lint(Bear):
    """
    :param executable:   The executable to run the linter.
    :param arguments:    The arguments to supply to the linter, such
                         that the file name to be analyzed can be
                         appended to the end.
    :param output_regex: The regex which will match the output of the linter
                         to get results. Thie regex should give out the
                         following variables:
                          line - The line where the issue starts.
                          column - The column where the issue starts.
                          end_line - The line where the issue ends.
                          end_column - The column where the issue ends.
                          severity - The severity of the issue.
                          message - The message of the result.
    :param use_stderr:   Uses stderr as the output stream is it's True.
    :param severity_map: A dict where the keys are the possible severity
                         values the Linter gives out and the values are the
                         severity of the coala Result to set it to. If it is
                         not a dict, it is ignored.
    """
    check_prerequisites = classmethod(is_binary_present)
    executable = None
    arguments = ""
    output_regex = re.compile(r'(?P<line>\d+)\.(?P<column>\d+)\|'
                              r'(?P<severity>\d+): (?P<message>.*)')
    use_stderr = False
    severity_map = None

    def lint(self, filename):
        """
        Takes a file and lints it using the linter variables defined apriori.

        :param filename: The name of the file to execute.
        """
        command = (self.executable + ' ' + self.arguments + ' '
                   + escape_path_argument(filename))
        stderr_file = tempfile.TemporaryFile()
        stdout_file = tempfile.TemporaryFile()
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=stdout_file,
            stderr=stderr_file,
            universal_newlines=True)
        process.wait()
        if self.use_stderr:
            stderr_file.seek(0)
            output = stderr_file.read().decode(sys.stdout.encoding,
                                               errors="replace")
        else:
            stdout_file.seek(0)
            output = stdout_file.read().decode(sys.stdout.encoding,
                                               errors="replace")
        stdout_file.close()
        stderr_file.close()
        return self.process_output(output, filename)

    def process_output(self, output, filename):
        regex = self.output_regex
        if isinstance(regex, str):
            regex = regex % {"file_name": filename}

        for match in re.finditer(regex, output):
            yield self.match_to_result(match, filename)

    def _get_groupdict(self, match):
        groups = match.groupdict()
        if (
                isinstance(self.severity_map, dict) and
                "severity" in groups and
                groups["severity"] in self.severity_map):
            groups["severity"] = self.severity_map[groups["severity"]]
        return groups

    def match_to_result(self, match, filename):
        """
        Converts a regex match's groups into a result.

        :param match:    The match got from regex parsing.
        :param filename: The name of the file from which this match is got.
        """
        groups = self._get_groupdict(match)

        # Pre process the groups
        for variable in ("line", "column", "end_line", "end_column"):
            if variable in groups and groups[variable]:
                groups[variable] = int(groups[variable])

        return Result.from_values(
            origin=groups.get("origin", self),
            message=groups.get("message", ""),
            file=filename,
            severity=int(groups.get("severity", RESULT_SEVERITY.NORMAL)),
            line=groups.get("line", None),
            column=groups.get("column", None),
            end_line=groups.get("end_line", None),
            end_column=groups.get("end_column", None))
