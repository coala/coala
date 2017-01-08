import difflib
from os.path import relpath, join

from pyprint.ConsolePrinter import ConsolePrinter

from coalib.results.Diff import ConflictError
from coalib.results.Result import Result
from coalib.results.result_actions.ResultAction import ResultAction

from coala_utils.decorators import enforce_signature


def format_line(line, real_nr='', sign='|', mod_nr='', symbol='', ):
    return '|{:>4}{}{:>4}|{:1}{}'.format(real_nr,
                                         sign,
                                         mod_nr,
                                         symbol,
                                         line.rstrip('\n'))


def print_from_name(printer, line):
    printer.print(format_line(line, real_nr='----'), color='red')


def print_to_name(printer, line):
    printer.print(format_line(line, mod_nr='++++'), color='green')


def print_beautified_diff(difflines, printer):
    current_line_added = None
    current_line_subtracted = None
    for line in difflines:
        if line.startswith('@@'):
            values = line[line.find('-'):line.rfind(' ')]
            subtracted, added = tuple(values.split(' '))
            current_line_added = int(added.split(',')[0][1:])
            current_line_subtracted = int(subtracted.split(',')[0][1:])
        elif line.startswith('---'):
            print_from_name(printer, line[4:])
        elif line.startswith('+++'):
            print_to_name(printer, line[4:])
        elif line.startswith('+'):
            printer.print(format_line(line[1:],
                                      mod_nr=current_line_added,
                                      symbol='+'),
                          color='green')
            current_line_added += 1
        elif line.startswith('-'):
            printer.print(format_line(line[1:],
                                      real_nr=current_line_subtracted,
                                      symbol='-'),
                          color='red')
            current_line_subtracted += 1
        else:
            printer.print(format_line(line[1:],
                                      real_nr=current_line_subtracted,
                                      mod_nr=current_line_added,
                                      symbol=' '))
            current_line_subtracted += 1
            current_line_added += 1


class ShowPatchAction(ResultAction):

    SUCCESS_MESSAGE = 'Displayed patch successfully.'

    @staticmethod
    @enforce_signature
    def is_applicable(result: Result, original_file_dict, file_diff_dict):

        if not result.diffs:
            return 'This result has no patch attached.'

        try:
            # Needed so the addition is run for all patches -> ConflictError
            nonempty_patches = False
            for filename, diff in result.diffs.items():
                if diff and (filename not in file_diff_dict or
                             diff + file_diff_dict[filename] !=
                             file_diff_dict[filename]):
                    nonempty_patches = True

            if nonempty_patches:
                return True
            return 'The given patches do not change anything anymore.'

        except ConflictError as ce:
            return ('Two or more patches conflict with '
                    'each other: {}'.format(str(ce)))

    def apply(self,
              result,
              original_file_dict,
              file_diff_dict,
              colored: bool=True,
              show_result_on_top: bool=False):
        """
        Show patch

        :param colored:
            Whether or not to use colored output.
        :param show_result_on_top:
            Set this to True if you want to show the result info on top.
            (Useful for e.g. coala_ci.)
        """
        printer = ConsolePrinter(colored)

        if show_result_on_top:
            from coalib.output.ConsoleInteraction import print_result
            # Most of the params are empty because they're unneeded in
            # noninteractive mode. Yes, this cries for a refactoring...
            print_result(printer, None, {}, result, {}, interactive=False)

        for filename, this_diff in sorted(result.diffs.items()):
            to_filename = this_diff.rename if this_diff.rename else filename
            to_filename = '/dev/null' if this_diff.delete else to_filename
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
