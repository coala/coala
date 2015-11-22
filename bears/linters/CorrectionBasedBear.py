from subprocess import Popen, PIPE

from coalib.bears.LocalBear import LocalBear
from coalib.results.Diff import Diff
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.results.Result import Result


class CorrectionBasedBear(LocalBear):
    SEVERITY = RESULT_SEVERITY.NORMAL
    GET_REPLACEMENT = (lambda self, file, cli_options:
                       self.__run_process(file, cli_options))

    def __run_process(self, file, cli_options):
        process = Popen(self.BINARY + ' ' + cli_options,
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
        for line in errors:
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
