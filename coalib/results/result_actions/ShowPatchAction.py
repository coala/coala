import difflib
from coalib.results.Diff import Diff
from coalib.results.result_actions.ResultAction import ResultAction
from coalib.results.Result import Result


class ShowPatchAction(ResultAction):
    @classmethod
    def is_applicable(cls, result):
        return isinstance(result, Result) and result.diffs is not None

    def apply(self, result, original_file_dict, file_diff_dict):
        """
        Print a unified diff of the patch that would be applied.
        """
        for filename, this_diff in sorted(result.diffs.items()):
            original_file = original_file_dict[filename]
            diff = file_diff_dict.get(filename, Diff())
            current_file = diff.apply(original_file)
            new_file = this_diff.apply(current_file)
            for line in difflib.unified_diff(current_file,
                                             new_file,
                                             fromfile=filename,
                                             tofile=filename):
                print(line, end="")

        return file_diff_dict
