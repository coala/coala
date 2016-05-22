import os
import re
import shlex
import shutil
from coalib.parsing.StringProcessing import escape
from subprocess import check_call, CalledProcessError, DEVNULL
import tempfile

from coalib.bears.Bear import Bear
from coala_decorators.decorators import enforce_signature
from coalib.misc.Shell import run_shell_command, get_shell_type
from coalib.results.Diff import Diff
from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


def escape_path_argument(path, shell=get_shell_type()):
    """
    Makes a raw path ready for using as parameter in a shell command (escapes
    illegal characters, surrounds with quotes etc.).

    :param path:  The path to make ready for shell.
    :param shell: The shell platform to escape the path argument for. Possible
                  values are "sh", "powershell", and "cmd" (others will be
                  ignored and return the given path without modification).
    :return:      The escaped path argument.
    """
    if shell == "cmd":
        # If a quote (") occurs in path (which is illegal for NTFS file
        # systems, but maybe for others), escape it by preceding it with
        # a caret (^).
        return '"' + escape(path, '"', '^') + '"'
    elif shell == "sh":
        return shlex.quote(path)
    else:
        # Any other non-supported system doesn't get a path escape.
        return path


class Lint(Bear):

    """
    Deals with the creation of linting bears.

    For the tutorial see:
    http://coala.readthedocs.org/en/latest/Users/Tutorials/Linter_Bears.html

    :param executable:                  The executable to run the linter.
    :param prerequisite_command:        The command to run as a prerequisite
                                        and is of type ``list``.
    :param prerequisites_fail_msg:      The message to be displayed if the
                                        prerequisite fails.
    :param arguments:                   The arguments to supply to the linter,
                                        such that the file name to be analyzed
                                        can be appended to the end. Note that
                                        we use ``.format()`` on the arguments -
                                        so, ``{abc}`` needs to be given as
                                        ``{{abc}}``. Currently, the following
                                        will be replaced:

                                         - ``{filename}`` - The filename passed
                                           to ``lint()``
                                         - ``{config_file}`` - The config file
                                           created using ``config_file()``

    :param output_regex:    The regex which will match the output of the linter
                            to get results. This is not used if
                            ``gives_corrected`` is set. This regex should give
                            out the following variables:

                             - line - The line where the issue starts.
                             - column - The column where the issue starts.
                             - end_line - The line where the issue ends.
                             - end_column - The column where the issue ends.
                             - severity - The severity of the issue.
                             - message - The message of the result.
                             - origin - The origin of the issue.

    :param diff_severity:   The severity to use for all results if
                            ``gives_corrected`` is set.
    :param diff_message:    The message to use for all results if
                            ``gives_corrected`` is set.
    :param use_stderr:      Uses stderr as the output stream is it's True.
    :param use_stdin:       Sends file as stdin instead of giving the file name.
    :param gives_corrected: True if the executable gives the corrected file
                            or just the issues.
    :param severity_map:    A dict where the keys are the possible severity
                            values the Linter gives out and the values are the
                            severity of the coala Result to set it to. If it is
                            not a dict, it is ignored.
    """
    executable = None
    prerequisite_command = None
    prerequisite_fail_msg = 'Unknown failure.'
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
        self.command = self._create_command(filename=filename,
                                            config_file=config_file)

        stdin_input = "".join(file) if self.use_stdin else None
        stdout_output, stderr_output = run_shell_command(self.command,
                                                         stdin=stdin_input,
                                                         shell=True)
        self.stdout_output = tuple(stdout_output.splitlines(keepends=True))
        self.stderr_output = tuple(stderr_output.splitlines(keepends=True))
        results_output = (self.stderr_output if self.use_stderr
                          else self.stdout_output)
        results = self.process_output(results_output, filename, file)
        if not self.use_stderr:
            self._print_errors(self.stderr_output)

        if config_file:
            os.remove(config_file)

        return results

    def process_output(self, output, filename, file):
        """
        Take the output (from stdout or stderr) and use it to create Results.
        If the class variable ``gives_corrected`` is set to True, the
        ``_process_corrected()`` is called. If it is False,
        ``_process_issues()`` is called.

        :param output:   The output to be used to obtain Results from. The
                         output is either stdout or stderr depending on the
                         class variable ``use_stderr``.
        :param filename: The name of the file whose output is being processed.
        :param file:     The contents of the file whose output is being
                         processed.
        :return:         Generator which gives Results produced based on this
                         output.
        """
        if self.gives_corrected:
            return self._process_corrected(output, filename, file)
        else:
            return self._process_issues(output, filename)

    def _process_corrected(self, output, filename, file):
        """
        Process the output and use it to create Results by creating diffs.
        The diffs are created by comparing the output and the original file.

        :param output:   The corrected file contents.
        :param filename: The name of the file.
        :param file:     The original contents of the file.
        :return:         Generator which gives Results produced based on the
                         diffs created by comparing the original and corrected
                         contents.
        """
        for diff in self.__yield_diffs(file, output):
            yield Result(self,
                         self.diff_message,
                         affected_code=(diff.range(filename),),
                         diffs={filename: diff},
                         severity=self.diff_severity)

    def _process_issues(self, output, filename):
        """
        Process the output using the regex provided in ``output_regex`` and
        use it to create Results by using named captured groups from the regex.

        :param output:   The output to be parsed by regex.
        :param filename: The name of the file.
        :param file:     The original contents of the file.
        :return:         Generator which gives Results produced based on regex
                         matches using the ``output_regex`` provided and the
                         ``output`` parameter.
        """
        regex = self.output_regex
        if isinstance(regex, str):
            regex = regex % {"file_name": filename}

        # Note: We join ``output`` because the regex may want to capture
        #       multiple lines also.
        for match in re.finditer(regex, "".join(output)):
            yield self.match_to_result(match, filename)

    def _get_groupdict(self, match):
        """
        Convert a regex match's groups into a dictionary with data to be used
        to create a Result. This is used internally in ``match_to_result``.

        :param match:    The match got from regex parsing.
        :param filename: The name of the file from which this match is got.
        :return:         The dictionary containing the information:
                         - line - The line where the result starts.
                         - column - The column where the result starts.
                         - end_line - The line where the result ends.
                         - end_column - The column where the result ends.
                         - severity - The severity of the result.
                         - message - The message of the result.
                         - origin - The origin of the result.
        """
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
        Convert a regex match's groups into a coala Result object.

        :param match:    The match got from regex parsing.
        :param filename: The name of the file from which this match is got.
        :return:         The Result object.
        """
        groups = self._get_groupdict(match)

        # Pre process the groups
        for variable in ("line", "column", "end_line", "end_column"):
            if variable in groups and groups[variable]:
                groups[variable] = int(groups[variable])

        if "origin" in groups:
            groups['origin'] = "{} ({})".format(str(self.name),
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

    @classmethod
    def check_prerequisites(cls):
        """
        Checks for prerequisites required by the Linter Bear.

        It uses the class variables:
        -  ``executable`` - Checks that it is available in the PATH using
        ``shutil.which``.
        -  ``prerequisite_command`` - Checks that when this command is run,
        the exitcode is 0. If it is not zero, ``prerequisite_fail_msg``
        is gives as the failure message.

        If either of them is set to ``None`` that check is ignored.

        :return: True is all checks are valid, else False.
        """
        return cls._check_executable_command(
            executable=cls.executable,
            command=cls.prerequisite_command,
            fail_msg=cls.prerequisite_fail_msg)

    @classmethod
    @enforce_signature
    def _check_executable_command(cls, executable,
                                  command: (list, tuple, None), fail_msg):
        """
        Checks whether the required executable is found and the
        required command succesfully executes.

        The function is intended be used with classes having an
        executable, prerequisite_command and prerequisite_fail_msg.

        :param executable:   The executable to check for.
        :param command:      The command to check as a prerequisite.
        :param fail_msg:     The fail message to display when the
                             command doesn't return an exitcode of zero.

        :return: True if command successfully executes, or is not required.
                 not True otherwise, with a string containing a
                 detailed description of the error.
        """
        if cls._check_executable(executable):
            if command is None:
                return True  # when there are no prerequisites
            try:
                check_call(command, stdout=DEVNULL, stderr=DEVNULL)
                return True
            except (OSError, CalledProcessError):
                return fail_msg
        else:
            return repr(executable) + " is not installed."

    @staticmethod
    def _check_executable(executable):
        """
        Checks whether the needed executable is present in the system.

        :param executable: The executable to check for.

        :return: True if binary is present, or is not required.
                 not True otherwise, with a string containing a
                 detailed description of what's missing.
        """
        if executable is None:
            return True
        return shutil.which(executable) is not None

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
        The section is available in ``self.section``. To add the config
        file's name generated by this function to the arguments,
        use ``{config_file}``.

        :return: A list of lines of the config file to be used or None.
        """
        return None
