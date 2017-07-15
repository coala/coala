import shutil
from os.path import isfile
from os import remove

from coalib.results.result_actions.ResultAction import ResultAction
from coalib.results.result_actions.ShowPatchAction import ShowPatchAction


class DoNothingAction(ResultAction):
    SUCCESS_MESSAGE = 'Patch applied successfully.'

    is_applicable = staticmethod(ShowPatchAction.is_applicable)

    def apply(self,
              result,
              original_file_dict,
              file_diff_dict):
        """
        *Do (N)othing
        """
        pass
