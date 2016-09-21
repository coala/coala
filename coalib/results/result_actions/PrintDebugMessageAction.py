from coalib.results.Result import Result
from coalib.results.result_actions.ResultAction import ResultAction


class PrintDebugMessageAction(ResultAction):

    @staticmethod
    def is_applicable(result, original_file_dict, file_diff_dict):
        return isinstance(result, Result) and result.debug_msg != ""

    def apply(self, result, original_file_dict, file_diff_dict):
        """
        Print debug message
        """
        print(result.debug_msg)

        return file_diff_dict
