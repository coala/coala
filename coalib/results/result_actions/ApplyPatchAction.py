import shutil

from coalib.results.result_actions.ResultAction import ResultAction
from coalib.results.Diff import ConflictError


class ApplyPatchAction(ResultAction):
    @staticmethod
    def is_applicable(result, original_file_dict, file_diff_dict):
        if not result.diffs:
            return False

        try:
            for filename in result.diffs:
                if filename in file_diff_dict:
                    result.diffs[filename].__add__(
                        file_diff_dict[filename])

            return True
        except ConflictError:
            return False

    def apply(self, result, original_file_dict, file_diff_dict):
        """
        Apply the patch automatically.
        """
        for filename in result.diffs:
            if filename in file_diff_dict:
                file_diff_dict[filename] += result.diffs[filename]
            else:
                file_diff_dict[filename] = result.diffs[filename]

            new_file = file_diff_dict[filename].modified

            # Backup original file, override old backup if needed
            shutil.copy2(filename, filename + ".orig")

            # Write new contents
            with open(filename, mode='w') as file:
                file.writelines(new_file)

        return file_diff_dict
