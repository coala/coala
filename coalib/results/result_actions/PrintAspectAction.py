from coalib.results.Result import Result
from coalib.results.result_actions.ResultAction import ResultAction


class PrintAspectAction(ResultAction):

    @staticmethod
    def is_applicable(result, original_file_dict, file_diff_dict):
        return isinstance(result, Result) and (result.aspect is not None)

    def apply(self, result, original_file_dict, file_diff_dict):
        """
        Print Aspect Information
        """
        print(result.aspect)

        return file_diff_dict
