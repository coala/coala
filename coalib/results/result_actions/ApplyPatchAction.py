import shutil
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

            new_file = file_diff_dict[filename].apply(
                original_file_dict[filename])

            # Backup original file, override old backup if needed
            shutil.copy2(filename, filename + ".orig")

            # Write new contents
            with open(filename, mode='w') as file:
                file.writelines(new_file)

        return file_diff_dict
