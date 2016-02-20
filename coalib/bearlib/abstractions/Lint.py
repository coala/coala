import os
import re
import shutil
import tempfile

from coalib.bears.Bear import Bear
from coalib.misc.Shell import escape_path_argument, run_shell_command
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
    Deals with the creation of linting bears.

    For the tutorial see:
    http://coala.readthedocs.org/en/latest/Users/Tutorials/Linter_Bears.html

    :param executable:      The executable to run the linter.
    :param arguments:       The arguments to supply to the linter, such
                            that the file name to be analyzed can be
                            appended to the end. Note that we use .format()
                            on the arguments - so, `{abc}` needs to be given
                            as `{{abc}}`.
                            Currently, the following will be replaced:
                            {filename}    - the filename passed to lint()
                            {config_file} - The config file created using
                                            config_file()
    :param output_regex:    The regex which will match the output of the linter
                            to get results. This regex should give out the
                            following variables:
                             line - The line where the issue starts.
                             column - The column where the issue starts.
                             end_line - The line where the issue ends.
                             end_column - The column where the issue ends.
                             severity - The severity of the issue.
                             message - The message of the result.
                             origin - The origin of the issue.
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

        config_file = self.generate_config_file()
        command = self._create_command(filename=filename,
                                       config_file=config_file)

        stdin_input = "".join(file) if self.use_stdin else None
        stdout_output, stderr_output = run_shell_command(command,
                                                         stdin=stdin_input)
        stdout_output = tuple(stdout_output.splitlines(keepends=True))
        stderr_output = tuple(stderr_output.splitlines(keepends=True))
        results_output = stderr_output if self.use_stderr else stdout_output
        results = self.process_output(results_output, filename, file)
        if not self.use_stderr:
            self._print_errors(stderr_output)

        if config_file:
            os.remove(config_file)

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

    def _create_command(self, **kwargs):
        command = self.executable + ' ' + self.arguments
        for key in ("filename", "config_file"):
            kwargs[key] = escape_path_argument(kwargs.get(key, "") or "")
        return command.format(**kwargs)

    def _print_errors(self, errors):
        for line in filter(lambda error: bool(error.strip()), errors):
            self.warn(line)

    @staticmethod
    def __yield_diffs(file, new_file):
        if tuple(new_file) != tuple(file):
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

        if "origin" in groups:
            groups['origin'] = "{} ({})".format(str(self.__class__.__name__),
                                                str(groups["origin"]))

        return Result.from_values(
            origin=groups.get("origin", self),
            message=groups.get("message", ""),
            file=filename,
            severity=int(groups.get("severity", RESULT_SEVERITY.NORMAL)),
            line=groups.get("line", None),
            column=groups.get("column", None),
            end_line=groups.get("end_line", None),
            end_column=groups.get("end_column", None))

    def generate_config_file(self):
        """
        Generates a temporary config file.
        Note: The user of the function is responsible for deleting the
        tempfile when done with it.

        :return: The file name of the tempfile created.
        """
        config_lines = self.config_file()
        config_file = ""
        if config_lines is not None:
            for i, line in enumerate(config_lines):
                config_lines[i] = line if line.endswith("\n") else line + "\n"
            config_fd, config_file = tempfile.mkstemp()
            os.close(config_fd)
            with open(config_file, 'w') as conf_file:
                conf_file.writelines(config_lines)
        return config_file

    @staticmethod
    def config_file():
        """
        Returns a configuation file from the section given to the bear.
        The section is available in `self.section`. To add the config
        file's name generated by this function to the arguments,
        use `{config_file}`.

        :return: A list of lines of the config file to be used or None.
        """
        return None
