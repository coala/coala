import subprocess

from coalib.results.Diff import Diff
from coalib.results.result_actions.ApplyPatchAction import ApplyPatchAction
from coalib.results.Result import Result


EDITOR_ARGS = {
    "subl": "--wait",
    "gedit": "-s"
}


GUI_EDITORS = ["kate", "gedit", "subl"]


class OpenEditorAction(ApplyPatchAction):
    @staticmethod
    def is_applicable(result):
        if isinstance(result, Result):
            if result.file is not None:
                return True
        return False

    def apply(self, result, original_file_dict, file_diff_dict, editor: str):
        '''
        Open the file in an editor.

        :param editor: The editor to open the file with.
        '''
        filename = result.file

        editor_args = [editor, filename]
        arg = EDITOR_ARGS.get(editor.strip(), None)
        if arg:
            editor_args.append(arg)

        # Dear user, you wanted an editor, so you get it. But do you really
        # think you can do better than we?
        if editor in GUI_EDITORS:
            subprocess.call(editor_args, stdout=subprocess.PIPE)
        else:
            subprocess.call(editor_args)

        with open(filename) as filehandle:
            new_file = filehandle.readlines()

        original_file = original_file_dict[filename]
        diff = file_diff_dict.get(filename, Diff())
        current_file = diff.apply(original_file)

        intermediate_diff = Diff.from_string_arrays(current_file, new_file)
        file_diff_dict[filename] = diff + intermediate_diff

        return file_diff_dict
