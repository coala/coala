from coalib.results.Result import Result
from coalib.results.result_actions.ResultAction import ResultAction


class PrintMoreInfoAction(ResultAction):

    @staticmethod
    def is_applicable(result, original_file_dict, file_diff_dict):
        return isinstance(result, Result) and result.additional_info != ""

    def apply(self, result, original_file_dict, file_diff_dict):
        """
        Print more info
        """
        print(result.additional_info)

        return file_diff_dict
