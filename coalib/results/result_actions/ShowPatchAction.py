import difflib

from coalib.results.Diff import Diff
from coalib.results.result_actions.ResultAction import ResultAction
from coalib.results.Result import Result


def print_beautified_diff(difflines):
    from coalib.output.ConsoleInteraction import format_line

    current_line_added = None
    current_line_subtracted = None
    for line in difflines:
        if line.startswith("@@"):
            values = line[line.find("-"):line.rfind(" ")]
            subtracted, added = tuple(values.split(" "))
            current_line_added = int(added.split(",")[0][1:])
            current_line_subtracted = int(subtracted.split(",")[0][1:])
        elif line.startswith("---") or line.startswith("+++"):
            print(format_line(line))
        elif line.startswith("+"):
            print(format_line(line[1:], mod_nr=current_line_added, symbol="+"))
            current_line_added += 1
        elif line.startswith("-"):
            print(format_line(line[1:],
                              real_nr=current_line_subtracted,
                              symbol="-"))
            current_line_subtracted += 1
        else:
            print(format_line(line[1:],
                              real_nr=current_line_subtracted,
                              mod_nr=current_line_added,
                              symbol=" "))
            current_line_subtracted += 1
            current_line_added += 1


class ShowPatchAction(ResultAction):
    @classmethod
    def is_applicable(cls, result):
        return isinstance(result, Result) and result.diffs is not None

    def apply(self, result, original_file_dict, file_diff_dict):
        """
        Print a unified diff of the patch that would be applied.
        """
        for filename, this_diff in sorted(result.diffs.items()):
            original_file = original_file_dict[filename]
            diff = file_diff_dict.get(filename, Diff())
            current_file = diff.apply(original_file)
            new_file = this_diff.apply(current_file)
            print_beautified_diff(difflib.unified_diff(current_file,
                                                       new_file,
                                                       fromfile=filename,
                                                       tofile=filename))

        return file_diff_dict
