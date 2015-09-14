from coalib.results.result_actions.ResultAction import ResultAction


class ApplyPatchAction(ResultAction):
    @staticmethod
    def is_applicable(result):
        return result.diffs is not None

    def apply(self, result, original_file_dict, file_diff_dict):
        """
        Apply the patch automatically.
        """
        for filename in result.diffs:
            if filename in file_diff_dict:
                file_diff_dict[filename] += result.diffs[filename]
            else:
                file_diff_dict[filename] = result.diffs[filename]

        return file_diff_dict
