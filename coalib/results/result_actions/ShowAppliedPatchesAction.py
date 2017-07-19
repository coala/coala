from coalib.results.result_actions.ResultAction import ResultAction
from coalib.results.result_actions.ShowPatchAction import ShowPatchAction
from coalib.results.RESULT_SEVERITY import (
    RESULT_SEVERITY, RESULT_SEVERITY_COLORS)
from pyprint.ConsolePrinter import ConsolePrinter


def format_lines(lines, symbol='', line_nr=''):
    def sym(x): return ']' if x is '[' else x
    return '\n'.join('{}{:>5}{} {}'.format(symbol, sym(symbol), line_nr, line)
                     for line in lines.rstrip('\n').split('\n'))


class ShowAppliedPatchesAction(ResultAction):

    SUCCESS_MESSAGE = 'All actions have been applied'

    is_applicable = staticmethod(ShowPatchAction.is_applicable)

    def apply(self,
              result,
              original_file_dict,
              file_diff_dict):
        """
        Show Applied (P)atches
        """
        console_printer = ConsolePrinter()
        applied_actions = result.get_applied_actions()
        show_patch_action = ShowPatchAction()
        RESULT_INDEX = 0
        FILE_DICT_INDEX = 1
        FILE_DIFF_DICT_INDEX = 2
        SECTION_INDEX = 3

        for key, val in applied_actions.items():
            this_result = val[RESULT_INDEX]
            this_section = val[SECTION_INDEX]
            color_res = RESULT_SEVERITY_COLORS[this_result.severity]
            console_printer.print('\n**** {bear} [Section: {section}] ***'
                                  '*\n**** Action Applied: {action} ****\n'
                                  .format(bear=this_result.origin,
                                          section=this_section.name,
                                          action=key),
                                  color=color_res)
            console_printer.print(format_lines('[Severity: {sev}]'.format(
                sev=RESULT_SEVERITY.__str__(this_result.severity)), '!'),
                  color=color_res)
            show_patch_action.apply_from_section(val[RESULT_INDEX],
                                                 val[FILE_DICT_INDEX],
                                                 val[FILE_DIFF_DICT_INDEX],
                                                 val[SECTION_INDEX])
            console_printer.print(
                '\n**************\n', color=color_res)
        return True
