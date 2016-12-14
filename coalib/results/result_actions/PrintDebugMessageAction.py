from coalib.results.Result import Result
from coalib.results.result_actions.ResultAction import ResultAction

from coala_utils.decorators import enforce_signature


class PrintDebugMessageAction(ResultAction):

    @staticmethod
    @enforce_signature
    def is_applicable(result: Result, original_file_dict, file_diff_dict):
        if result.debug_msg != '':
            return True
        return 'There is no debug message.'

    def apply(self, result, original_file_dict, file_diff_dict):
        """
        Print debug message
        """
        print(result.debug_msg)

        return file_diff_dict
