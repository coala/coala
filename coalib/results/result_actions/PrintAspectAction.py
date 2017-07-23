from coalib.results.Result import Result
from coalib.results.result_actions.ResultAction import ResultAction

from coala_utils.decorators import enforce_signature


class PrintAspectAction(ResultAction):

    @staticmethod
    @enforce_signature
    def is_applicable(result: Result, original_file_dict, file_diff_dict):
        if result.aspect is None:
            return 'There is no aspect associated with the result.'
        return True

    def apply(self, result, original_file_dict, file_diff_dict):
        """
        Print Aspec(T) Information
        """
        aspect_info = (type(result.aspect).__qualname__ + ':\n' +
                       '    ' + type(result.aspect).docs.definition)
        print('This code does not comply to ' + aspect_info)

        return file_diff_dict
