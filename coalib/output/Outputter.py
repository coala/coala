from coalib.bears.results.LineResult import Result, LineResult


class Outputter:
    def _print_result(self, result):
        raise NotImplementedError

    def _print_line_result(self, result):
        # You probably want to overwrite this method!
        return self._print_result(result)

    def print_result(self, result):
        """
        Prints the result appropriate to the output medium.

        :param result: A derivative of Result.
        """
        if not isinstance(result, Result):
            raise TypeError("print_result can only handle objects which inherit from Result.")

        if type(result) == LineResult:
            return self._print_line_result(result)

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
