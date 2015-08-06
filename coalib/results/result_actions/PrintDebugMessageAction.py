from coalib.results.result_actions.ResultAction import ResultAction
from coalib.results.Result import Result


class PrintDebugMessageAction(ResultAction):
    @staticmethod
    def is_applicable(result):
        return isinstance(result, Result) and result.debug_msg != ""

    def apply(self, result, original_file_dict, file_diff_dict):
        """
        Print the debug message of the result.
        """
        print(result.debug_msg)

        return file_diff_dict
