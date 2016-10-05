import shutil
from os.path import isfile
from os import remove

from coalib.results.result_actions.ShowPatchAction import ShowPatchAction
from coalib.results.result_actions.ResultAction import ResultAction


class ApplyPatchAction(ResultAction):

    SUCCESS_MESSAGE = "Patch applied successfully."

    is_applicable = staticmethod(ShowPatchAction.is_applicable)

    def apply(self,
              result,
              original_file_dict,
              file_diff_dict,
              no_orig: bool=False):
        """
        Apply patch

        :param no_orig: Whether or not to create .orig backup files
        """
        for filename in result.diffs:
            pre_patch_filename = filename
            if filename in file_diff_dict:
                diff = file_diff_dict[filename]
                pre_patch_filename = (diff.rename
                                      if diff.rename is not False
                                      else filename)
                file_diff_dict[filename] += result.diffs[filename]
            else:
                file_diff_dict[filename] = result.diffs[filename]

                # Backup original file, only if there was no previous patch
                # from this run though!
                if not no_orig and isfile(pre_patch_filename):
                    shutil.copy2(pre_patch_filename,
                                 pre_patch_filename + ".orig")

            diff = file_diff_dict[filename]
            if diff.delete or diff.rename:
                if isfile(pre_patch_filename):
                    remove(pre_patch_filename)
            if not diff.delete:
                new_filename = (diff.rename
                                if diff.rename is not False
                                else filename)
                with open(new_filename, mode='w', encoding='utf-8') as file:
                    file.writelines(diff.modified)

        return file_diff_dict
