import difflib
from os.path import relpath, join

from pyprint.ConsolePrinter import ConsolePrinter

from coalib.results.Diff import ConflictError
from coalib.results.Result import Result
from coalib.results.result_actions.ResultAction import ResultAction


def format_line(line, real_nr="", sign="|", mod_nr="", symbol="", ):
    return "|{:>4}{}{:>4}|{:1}{}".format(real_nr,
                                         sign,
                                         mod_nr,
                                         symbol,
                                         line.rstrip("\n"))


def print_from_name(printer, line):
    printer.print(format_line(line, real_nr="----"), color="red")


def print_to_name(printer, line):
    printer.print(format_line(line, mod_nr="++++"), color="green")


def print_beautified_diff(difflines, printer):
    current_line_added = None
    current_line_subtracted = None
    for line in difflines:
        if line.startswith("@@"):
            values = line[line.find("-"):line.rfind(" ")]
            subtracted, added = tuple(values.split(" "))
            current_line_added = int(added.split(",")[0][1:])
            current_line_subtracted = int(subtracted.split(",")[0][1:])
        elif line.startswith("---"):
            print_from_name(printer, line[4:])
        elif line.startswith("+++"):
            print_to_name(printer, line[4:])
        elif line.startswith("+"):
            printer.print(format_line(line[1:],
                                      mod_nr=current_line_added,
                                      symbol="+"),
                          color="green")
            current_line_added += 1
        elif line.startswith("-"):
            printer.print(format_line(line[1:],
                                      real_nr=current_line_subtracted,
                                      symbol="-"),
                          color="red")
            current_line_subtracted += 1
        else:
            printer.print(format_line(line[1:],
                                      real_nr=current_line_subtracted,
                                      mod_nr=current_line_added,
                                      symbol=" "))
            current_line_subtracted += 1
            current_line_added += 1


class ShowPatchAction(ResultAction):

    SUCCESS_MESSAGE = "Displayed patch successfully."

    @staticmethod
    def is_applicable(result, original_file_dict, file_diff_dict):
        if not isinstance(result, Result) or not result.diffs:
            return False

        try:
            for filename in result.diffs:
                if filename in file_diff_dict:
                    result.diffs[filename].__add__(file_diff_dict[filename])
            return True
        except ConflictError:
            return False

    def apply(self,
              result,
              original_file_dict,
              file_diff_dict,
              colored: bool=True):
        """
        Print a diff of the patch that would be applied.
        :param colored: Whether or not to use colored output.
        """
        printer = ConsolePrinter(colored)

        for filename, this_diff in sorted(result.diffs.items()):
            to_filename = this_diff.rename if this_diff.rename else filename
            to_filename = "/dev/null" if this_diff.delete else to_filename
            original_file = original_file_dict[filename]
            try:
                current_file = file_diff_dict[filename].modified
                new_file = (file_diff_dict[filename] + this_diff).modified
            except KeyError:
                current_file = original_file
                new_file = this_diff.modified

            if tuple(current_file) != tuple(new_file):
                print_beautified_diff(difflib.unified_diff(current_file,
                                                           new_file,
                                                           fromfile=filename,
                                                           tofile=to_filename),
                                      printer)
            elif filename != to_filename:
                print_from_name(printer, join('a', relpath(filename)))
                print_to_name(printer, join('b', relpath(to_filename)))

        return file_diff_dict
