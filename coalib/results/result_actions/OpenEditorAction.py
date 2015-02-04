import os
import tempfile

from coalib.results.Diff import Diff
from coalib.results.result_actions.ApplyPatchAction import ApplyPatchAction


class OpenEditorAction(ApplyPatchAction):
    def apply(self, result, original_file_dict, file_diff_dict, editor: str):
        """
        Open the file in an editor.

        :param editor: The editor to open the file with.
        """
        filename = result.file
        original_file = original_file_dict[filename]
        diff = file_diff_dict.get(filename, Diff())
        current_file = diff.apply(original_file)

        # Prefix is nice for the user so he has an indication that its the right file he's editing
        tempfile_handle, tempfile_name = tempfile.mkstemp(prefix=filename)
        os.close(tempfile_handle)
        with open(tempfile_name, "w") as tempfile_handle:
            tempfile_handle.writelines(current_file)

        # Dear user, you wanted an editor, so you get it. But do you really think you can do better than we?
        os.system(editor + " " + tempfile_name)

        with open(tempfile_name) as tempfile_handle:
            new_file = tempfile_handle.readlines()

        os.remove(tempfile_name)

        intermediate_diff = Diff.from_string_arrays(current_file, new_file)
        file_diff_dict[filename] = diff + intermediate_diff

        return file_diff_dict
