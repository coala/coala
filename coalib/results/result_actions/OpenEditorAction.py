import os
import tempfile

from coalib.results.Diff import Diff
from coalib.results.result_actions.ApplyPatchAction import ApplyPatchAction

EDITOR_ARGS = {
    "subl" : "--wait",
    "gedit" : "-s"
}


class OpenEditorAction(ApplyPatchAction):
    def apply(self, result, original_file_dict, file_diff_dict, editor: str):
        """
        Open a temporary clone of the file in an editor.

        :param editor: The editor to open the file with.
        """
        filename = result.file
        original_file = original_file_dict[filename]
        diff = file_diff_dict.get(filename, Diff())
        current_file = diff.apply(original_file)

        # Prefix is nice for the user so he has an indication that its the
        # right file he's editing
        temphandle, tempname = tempfile.mkstemp(os.path.basename(filename))
        os.close(temphandle)
        with open(tempname, "w") as temphandle:
            temphandle.writelines(current_file)

        editor_arg = EDITOR_ARGS.get(editor.strip(), None)
        if editor_arg:
            editor = editor + " " + editor_arg

        # Dear user, you wanted an editor, so you get it. But do you really
        # think you can do better than we?
        os.system(editor + " " + tempname)

        with open(tempname) as temphandle:
            new_file = temphandle.readlines()

        os.remove(tempname)

        intermediate_diff = Diff.from_string_arrays(current_file, new_file)
        file_diff_dict[filename] = diff + intermediate_diff

        return file_diff_dict
