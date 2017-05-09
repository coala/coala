from coalib.results.Result import Result
from coalib.results.result_actions.ResultAction import ResultAction


class PrintAspectDescriptionAction(ResultAction):

    @staticmethod
    def is_applicable(result, original_file_dict, file_diff_dict):
        return isinstance(result, Result)

    def apply(self, result, original_file_dict, file_diff_dict):
        """

        Print Aspect description
        """
        print(result.aspect.__qualname__)
        print(result.aspect.desc)

        return file_diff_dict
