import subprocess
from os.path import exists

from coalib.results.Diff import Diff
from coalib.results.Result import Result
from coalib.results.result_actions.ResultAction import ResultAction

EDITOR_ARGS = {
    "subl": "--wait",
    "gedit": "-s",
    "atom": "--wait"
}


GUI_EDITORS = ["kate", "gedit", "subl", "atom"]


class OpenEditorAction(ResultAction):

    SUCCESS_MESSAGE = "Changes saved successfully."

    @staticmethod
    def is_applicable(result, original_file_dict, file_diff_dict):
        """
        For being applicable, the result has to point to a number of files
        that have to exist i.e. have not been previously deleted.
        """
        if not isinstance(result, Result) or not len(result.affected_code) > 0:
            return False

        filenames = set(src.renamed_file(file_diff_dict)
                        for src in result.affected_code)
        return all(exists(filename) for filename in filenames)

    def apply(self, result, original_file_dict, file_diff_dict, editor: str):
        """
        Open the affected file(s) in an editor.

        :param editor: The editor to open the file with.
        """
        # Use set to remove duplicates
        filenames = {src.file: src.renamed_file(file_diff_dict)
                     for src in result.affected_code}

        editor_args = [editor] + list(filenames.values())
        arg = EDITOR_ARGS.get(editor.strip(), None)
        if arg:
            editor_args.append(arg)

        # Dear user, you wanted an editor, so you get it. But do you really
        # think you can do better than we?
        if editor in GUI_EDITORS:
            subprocess.call(editor_args, stdout=subprocess.PIPE)
        else:
            subprocess.call(editor_args)

        for original_name, filename in filenames.items():
            with open(filename, encoding='utf-8') as file:
                file_diff_dict[original_name] = Diff.from_string_arrays(
                    original_file_dict[original_name], file.readlines(),
                    rename=False if original_name == filename else filename)

        return file_diff_dict
