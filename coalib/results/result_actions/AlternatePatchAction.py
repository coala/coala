from coalib.results.Result import Result
from coalib.results.result_actions.ResultAction import ResultAction
from coalib.results.result_actions.ShowPatchAction import ShowPatchAction


class AlternatePatchAction(ResultAction):

    SUCCESS_MESSAGE = 'Displayed patch successfully.'

    def __init__(self, diffs, count):
        self.diffs = diffs
        self.description = 'Show Alternate Patch ' + str(count)

    def is_applicable(self,
                      result: Result,
                      original_file_dict,
                      file_diff_dict,
                      applied_actions=()):
        return 'ApplyPatchAction' not in applied_actions

    def apply(self,
              result,
              original_file_dict,
              file_diff_dict,
              no_color: bool = False):
        self.diffs, result.diffs = result.diffs, self.diffs
        self.update_description(result)
        return ShowPatchAction().apply(result,
                                       original_file_dict,
                                       file_diff_dict,
                                       no_color=no_color)

    def update_description(self, result):
        alternate_diffs = result.alternate_diffs
        if self.diffs in alternate_diffs:
            count = alternate_diffs.index(self.diffs) + 1
            self.description = 'Show Alternate Patch ' + str(count)
        else:
            self.description = 'Show Original Patch'
