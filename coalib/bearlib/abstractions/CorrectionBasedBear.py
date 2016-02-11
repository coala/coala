import shutil
from subprocess import PIPE, Popen

from coalib.bears.LocalBear import LocalBear
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


class CorrectionBasedBear(LocalBear):
    check_prerequisites = classmethod(is_binary_present)
    SEVERITY = RESULT_SEVERITY.NORMAL
    GET_REPLACEMENT = (lambda self, file, cli_options:
                       self.__run_process(file, cli_options))

    def __run_process(self, file, cli_options):
        process = Popen(self.executable + ' ' + cli_options,
                        shell=True,
                        stdin=PIPE,
                        stdout=PIPE,
                        stderr=PIPE,
                        universal_newlines=True)
        process.stdin.writelines(file)
        process.stdin.close()
        process.wait()

        corrected = process.stdout.readlines()
        errors = process.stderr.readlines()

        process.stdout.close()
        process.stderr.close()

        return corrected, errors

    @staticmethod
    def __yield_diffs(file, new_file):
        if new_file != file:
            wholediff = Diff.from_string_arrays(file, new_file)

            for diff in wholediff.split_diff():
                yield diff

    def __print_errors(self, errors):
        for line in filter(lambda error: bool(error.strip()), errors):
            self.warn(line)

    def retrieve_results(self, filename, file, **kwargs):
        """
        Yields results using the self.GET_REPLACEMENT function.

        :param filename: The filename, just pass it over as you got it!
        :param file:     The file, just pass it over as you got it!
        :param kwargs:   Any keyword arguments that will be passed to the
                         GET_REPLACEMENT function. Please provide cli_options
                         if you don't override the default.
        """
        new_file, errors = self.GET_REPLACEMENT(file=file, **kwargs)
        self.__print_errors(errors)

        for diff in self.__yield_diffs(file, new_file):
            yield Result(
                self,
                self.RESULT_MESSAGE,
                affected_code=(diff.range(filename),),
                diffs={filename: diff},
                severity=self.SEVERITY)
