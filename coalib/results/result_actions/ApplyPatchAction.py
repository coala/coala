import shutil
from os.path import isfile
from os import remove

from coalib.results.Diff import ConflictError
from coalib.results.result_actions.ResultAction import ResultAction


class ApplyPatchAction(ResultAction):

    SUCCESS_MESSAGE = "Patch applied successfully."

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

    def apply(self,
              result,
              original_file_dict,
              file_diff_dict,
              no_orig: bool=False):
        """
        Apply the patch automatically.

        :param no_orig: Whether or not to create .orig backup files
        """
        for filename in result.diffs:
            diff = file_diff_dict[filename]
            pre_patch_filename = (diff.rename
                                  if diff.rename is not False
                                  else filename)
            if filename in file_diff_dict:
                file_diff_dict[filename] += result.diffs[filename]
            else:
                file_diff_dict[filename] = result.diffs[filename]

            # Backup file, backups are deleted on startup -> don't override
            if not no_orig and not isfile(pre_patch_filename + ".orig"):
                shutil.copy2(pre_patch_filename, pre_patch_filename + ".orig")

            diff = file_diff_dict[filename]
            if diff.delete:
                remove(pre_patch_filename)
            else:
                new_filename = (diff.rename
                                if diff.rename is not False
                                else filename)
                with open(new_filename, mode='w', encoding='utf-8') as file:
                    file.writelines(diff.modified)

        return file_diff_dict
