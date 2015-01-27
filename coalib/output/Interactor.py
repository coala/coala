from coalib.bearlib.abstractions.SectionCreatable import SectionCreatable
from coalib.results.Result import Result
from coalib.output.printers.ConsolePrinter import ConsolePrinter
from coalib.misc.i18n import _
from coalib.settings.FunctionMetadata import FunctionMetadata


class Interactor(SectionCreatable):
    def __init__(self, log_printer=ConsolePrinter()):
        SectionCreatable.__init__(self)
        self.log_printer = log_printer
        self.file_diff_dict = {}

    def _print_result(self, result):
        raise NotImplementedError

    def print_result(self, result):
        """
        Prints the result appropriate to the output medium.

        :param result: A derivative of Result.
        """
        if not isinstance(result, Result):
            self.log_printer.warn(_("One of the results can not be printed since it is not a valid derivative of the "
                                    "coala result class."))
            return

        return self._print_result(result)

    def print_results(self, result_list, file_dict):
        """
        Prints all given results. They will be sorted.

        :param result_list: List of the results
        :param file_dict: Dictionary containing filename: file_contents
        """
        if not isinstance(result_list, list):
            raise TypeError("result_list should be of type list")
        if not isinstance(file_dict, dict):
            raise TypeError("file_dict should be of type dict")

        sorted_results = sorted(result_list)
        for result in sorted_results:
            self.print_result(result)

    def acquire_settings(self, settings):
        """
        This method prompts the user for the given settings.

        :param settings: a dictionary with the settings name as key and a list containing a description in [0] and the
                         name of the bears who need this setting in [1] and following. Example:
        {"UseTabs": ["describes whether tabs should be used instead of spaces",
                     "SpaceConsistencyBear",
                     "SomeOtherBear"]}

        :return: a dictionary with the settings name as key and the given value as value.
        """
        raise NotImplementedError

    def finalize(self, file_dict):
        """
        To be called after all results are given to the interactor.
        """
        for filename in self.file_diff_dict:
            diff = self.file_diff_dict[filename]
            file_dict[filename] = diff.apply(file_dict[filename])

            with open(filename, mode='w') as file:
                file.writelines(file_dict[filename])

    @classmethod
    def get_metadata(cls):
        return FunctionMetadata.from_function(cls.__init__, ["self", "log_printer"])
