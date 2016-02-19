import subprocess

from coalib.results.Diff import Diff
from coalib.results.Result import Result
from coalib.results.result_actions.ApplyPatchAction import ApplyPatchAction

EDITOR_ARGS = {
    "subl": "--wait",
    "gedit": "-s",
    "atom": "--wait"
}


GUI_EDITORS = ["kate", "gedit", "subl", "atom"]


class OpenEditorAction(ApplyPatchAction):

    success_message = "Changes saved successfully."

    @staticmethod
    def is_applicable(result, original_file_dict, file_diff_dict):
        return isinstance(result, Result) and len(result.affected_code) > 0

    def apply(self, result, original_file_dict, file_diff_dict, editor: str):
        '''
        Open the affected file(s) in an editor.

        :param editor: The editor to open the file with.
        '''
        # Use set to remove duplicates
        filenames = set(src.file for src in result.affected_code)

        editor_args = [editor] + list(filenames)
        arg = EDITOR_ARGS.get(editor.strip(), None)
        if arg:
            editor_args.append(arg)

        # Dear user, you wanted an editor, so you get it. But do you really
        # think you can do better than we?
        if editor in GUI_EDITORS:
            subprocess.call(editor_args, stdout=subprocess.PIPE)
        else:
            subprocess.call(editor_args)

        for filename in filenames:
            with open(filename, encoding='utf-8') as file:
                new_file = file.readlines()

            original_file = original_file_dict[filename]
            try:
                current_file = file_diff_dict[filename].modified
            except KeyError:
                current_file = original_file

            file_diff_dict[filename] = Diff.from_string_arrays(original_file,
                                                               new_file)

        return file_diff_dict
