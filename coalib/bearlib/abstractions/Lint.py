import re
import shutil
import subprocess
import sys
import tempfile

from coalib.bears.Bear import Bear
from coalib.misc.Shell import escape_path_argument
from coalib.results.Diff import Diff
from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


def is_binary_present(cls):
    """
    Checks whether the needed binary is present.

    The function is intended be used with classes
    having an executable member which will be checked.

    :return: True if binary is present, or is not required.
             not True otherwise, with a string containing a
             detailed description of what's missing.
    """
    try:
        if cls.executable is None:
            return True
        if shutil.which(cls.executable) is None:
            return repr(cls.executable) + " is not installed."
        else:
            return True
    except AttributeError:
        # Happens when `executable` does not exist in `cls`.
        return True


class Lint(Bear):
    """
    :param executable:      The executable to run the linter.
    :param arguments:       The arguments to supply to the linter, such
                            that the file name to be analyzed can be
                            appended to the end.
    :param output_regex:    The regex which will match the output of the linter
                            to get results. This regex should give out the
                            following variables:
                             line - The line where the issue starts.
                             column - The column where the issue starts.
                             end_line - The line where the issue ends.
                             end_column - The column where the issue ends.
                             severity - The severity of the issue.
                             message - The message of the result.
                            This is not used if `gives_corrected` is set.
    :param diff_severity:   The severity to use for all results if
                            `gives_corrected` is set.
    :param diff_message:    The message to use for all results if
                            `gives_corrected` is set.
    :param use_stderr:      Uses stderr as the output stream is it's True.
    :param use_stdin:       Sends file as stdin instead of giving the file name.
    :param gives_corrected: True if the executable gives the corrected file
                            or just the issues.
    :param severity_map:    A dict where the keys are the possible severity
                            values the Linter gives out and the values are the
                            severity of the coala Result to set it to. If it is
                            not a dict, it is ignored.
    """
    check_prerequisites = classmethod(is_binary_present)
    executable = None
    arguments = ""
    output_regex = re.compile(r'(?P<line>\d+)\.(?P<column>\d+)\|'
                              r'(?P<severity>\d+): (?P<message>.*)')
    diff_message = 'No result message was set'
    diff_severity = RESULT_SEVERITY.NORMAL
    use_stderr = False
    use_stdin = False
    gives_corrected = False
    severity_map = None

    def lint(self, filename=None, file=None):
        """
        Takes a file and lints it using the linter variables defined apriori.

        :param filename:  The name of the file to execute.
        :param file:      The contents of the file as a list of strings.
        """
        assert ((self.use_stdin and file is not None) or
                (not self.use_stdin and filename is not None))

        stdin_file = tempfile.TemporaryFile()
        stdout_file = tempfile.TemporaryFile()
        stderr_file = tempfile.TemporaryFile()

        command = self._create_command(filename)

        if self.use_stdin:
            self._write(file, stdin_file, sys.stdin.encoding)
        process = subprocess.Popen(command,
                                   shell=True,
                                   stdin=stdin_file,
                                   stdout=stdout_file,
                                   stderr=stderr_file,
                                   universal_newlines=True)
        process.wait()
        stdout_output = self._read(stdout_file, sys.stdout.encoding)
        stderr_output = self._read(stderr_file, sys.stderr.encoding)
        results_output = stderr_output if self.use_stderr else stdout_output
        results = self.process_output(results_output, filename, file)
        for file in (stdin_file, stdout_file, stderr_file):
            file.close()

        if not self.use_stderr:
            self.__print_errors(stderr_output)

        return results

    def process_output(self, output, filename, file):
        if self.gives_corrected:
            return self._process_corrected(output, filename, file)
        else:
            return self._process_issues(output, filename)

    def _process_corrected(self, output, filename, file):
        for diff in self.__yield_diffs(file, output):
            yield Result(self,
                         self.diff_message,
                         affected_code=(diff.range(filename),),
                         diffs={filename: diff},
                         severity=self.diff_severity)

    def _process_issues(self, output, filename):
        regex = self.output_regex
        if isinstance(regex, str):
            regex = regex % {"file_name": filename}

        # Note: We join `output` because the regex may want to capture
        #       multiple lines also.
        for match in re.finditer(regex, "".join(output)):
            yield self.match_to_result(match, filename)

    def _get_groupdict(self, match):
        groups = match.groupdict()
        if (
                isinstance(self.severity_map, dict) and
                "severity" in groups and
                groups["severity"] in self.severity_map):
            groups["severity"] = self.severity_map[groups["severity"]]
        return groups

    def _create_command(self, filename):
        command = self.executable + ' ' + self.arguments
        if not self.use_stdin:
            command += ' ' + escape_path_argument(filename)
        return command

    @staticmethod
    def _read(file, encoding):
        file.seek(0)
        return [line.decode(encoding or 'UTF-8', errors="replace")
                for line in file.readlines()]

    @staticmethod
    def _write(file_contents, file, encoding):
        file.write(bytes("".join(file_contents), encoding or 'UTF-8'))
        file.seek(0)

    def __print_errors(self, errors):
        for line in filter(lambda error: bool(error.strip()), errors):
            self.warn(line)

    @staticmethod
    def __yield_diffs(file, new_file):
        if new_file != file:
            wholediff = Diff.from_string_arrays(file, new_file)

            for diff in wholediff.split_diff():
                yield diff

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
