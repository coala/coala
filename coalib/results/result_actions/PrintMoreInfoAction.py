from coalib.results.Result import Result
from coalib.results.result_actions.ResultAction import ResultAction

from coala_utils.decorators import enforce_signature


class PrintMoreInfoAction(ResultAction):

    @staticmethod
    @enforce_signature
    def is_applicable(result: Result, original_file_dict, file_diff_dict):
        if result.additional_info != '':
            return True
        return 'There is no additional info.'

    def apply(self, result, original_file_dict, file_diff_dict):
        """
        Print more info
        """
        print(result.additional_info)

        return file_diff_dict
