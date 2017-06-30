from coalib.results.result_actions.ResultAction import ResultAction
from coalib.results.result_actions.ShowPatchAction import ShowPatchAction


class ChainPatchAction(ResultAction):

    SUCCESS_MESSAGE = 'All actions have been applied'

    is_applicable = staticmethod(ShowPatchAction.is_applicable)

    def apply(self,
              result,
              original_file_dict,
              file_diff_dict,
              actions: str):
        """
        (C)hain actions

        :param actions: A string of all actions.
        """
