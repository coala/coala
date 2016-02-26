import os
import re
import shutil
import tempfile

from coalib.bears.LocalBear import LocalBear
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


class LinterHandler:
    def create_arguments(self, filename, file, config_file): # TODO Also file???
        raise NotImplementedError

    def generate_config(self):
        return None


# TODO Dynamic kwargs usage. Context depending signature.
# TODO --> But maybe not, this allows for @enforce_signature
# TODO ------> Or "hybrid" approach, needed arguments are optional, if one activates
# TODO ------> further options these get passed by kwargs
def Linter(executable, **kwargs):
    kwargs["executable"] = executable # TODO Sucks...
    def create_linter(cls):
        class Linter(LocalBear):

            # TODO Override __repr__ since the name of the class shall be the
            # TODO same like the one used for the LinterHandler

            @property
            def handler(self):
                return cls # TODO Directly import functions? Rethink design maybe then...
            @property
            def executable(self):
                return kwargs["executable"] # TODO This needs to be solved more elegant...

            def _execute_command(self, args, stdin=None):
                # TODO Also more elegance...
                return run_shell_command((kwargs["executable"],) + tuple(args),
                                         stdin=stdin)

            if kwargs["provides_correction"]:
                @staticmethod
                def _process_output(output, filename, file):
                    pass  # Process an entire corrected file from output
            else:
                @staticmethod
                def _process_output(output, filename, file):
                    pass  # Process normal issue warnings

            if kwargs["use_stderr"]:
                @staticmethod
                def _grab_output(stdout, stderr):
                    return stderr
            else:
                @staticmethod
                def _grab_output(stdout, stderr):
                    return stdout

            if kwargs["use_stdin"]:
                @staticmethod
                def _pass_file_as_stdin_if_needed(file):
                    return file
            else:
                @staticmethod
                def _pass_file_as_stdin_if_needed(file):
                    return None

            def run(self, filename, file):
                # TODO Generate config_file here if used
                stdout, stderr = self._execute_command(
                    self.handler.create_arguments(filename, file),
                    stdin=self._pass_file_as_stdin_if_needed(file))
                output = self._grab_output(stdout, stderr)
                self._process_output(output, filename, file)

        return Linter

    return create_linter


class Lint(Bear):
    """
    Deals with the creation of linting bears.

    For the tutorial see:
    http://coala.readthedocs.org/en/latest/Users/Tutorials/Linter_Bears.html

    :param executable:      The executable to run the linter.
    :param shell:           Whether to execute the executable in shell. `False`
                            by default.
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
    shell = False
    output_regex = re.compile(r'(?P<line>\d+)\.(?P<column>\d+)\|'
                              r'(?P<severity>\d+): (?P<message>.*)')
    diff_message = 'No result message was set'
    diff_severity = RESULT_SEVERITY.NORMAL
    use_stderr = False
    use_stdin = False
    gives_corrected = False
    severity_map = None

    # TODO: Lint IS ONLY FOR SINGLE FILE INPUT!!!
    # TODO: When refactoring to functions, provide a setup_lint() function
    #       that uses functools.partial() to cache fixed parameters (like
    #       use_stdin or the severity_map). Whether to only allow
    #       executable_args to be passed then or also other kwargs needs to
    #       be investigated^^
    # TODO: Document whether gives_corrected also requires `file` for kwargs!
    def lint(self, executable_args, filename, **kwargs):
        """
        Takes a file and lints it using the linter variables defined apriori.

        If `use_stdin` is `True` it's mandatory to provide `file` as `kwargs`
        that contains the file-contents as a string to send to the underlying
        tool.

        :param executable_args: The arguments to pass to the executable. This
                                can be either a sequence or a string (in this
                                case the arguments are splitted using
                                `shlex.split()`).

                                Sequences are preferred as `shlex.split()`
                                resembles linux-shell behaviour which
                                recognizes backslash as an escape character. On
                                Windows paths are separated using backslashes,
                                so passing the path directly inside a sequence
                                avoids correctly escaping paths.
        :param kwargs:          Special key-value arguments used for specific
                                settings. See details of `lint()`.
        :raises RuntimeError:   Raised when `self.use_stdin` is `True` but no
                                file-content was provided via in `kwargs` with
                                `file`.
        """
        if self.use_stdin and not "file" in kwargs:
            raise RuntimeError("use_stdin specified but no `file` provided "
                               "inside `kwargs`.")

        config_file = self.generate_config_file()

        stdin_input = kwargs["file"] if self.use_stdin else None
        stdout_output, stderr_output = run_shell_command(
            self._create_command(executable_args),
            stdin=stdin_input,
            shell=self.shell)

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

    def _create_command(self, args):
        if isinstance(args, str):
            return self.executable + " " + self.arguments
        else:
            return (self.executable,) + tuple(args)

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
