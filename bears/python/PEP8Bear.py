import autopep8

from coalib.bearlib.abstractions.CorrectionBasedBear import CorrectionBasedBear
from coalib.bearlib.spacing.SpacingHelper import SpacingHelper
from coalib.settings.Setting import typed_list


class PEP8Bear(CorrectionBasedBear):
    RESULT_MESSAGE = "The code does not comply to PEP8."

    @staticmethod
    def run_autopep(file,
                    pep_ignore,
                    pep_select,
                    max_line_length,
                    indent_size):
        new_file = autopep8.fix_code(
            ''.join(file),
            options={'ignore': pep_ignore,
                     'select': pep_select,
                     'max_line_length': max_line_length,
                     'indent_size': indent_size})

        return new_file.splitlines(True), []

    GET_REPLACEMENT = run_autopep

    def run(self,
            filename,
            file,
            max_line_length: int=80,
            tab_width: int=SpacingHelper.DEFAULT_TAB_WIDTH,
            pep_ignore: typed_list(str)=(),
            pep_select: typed_list(str)=()):
        """
        Detects and fixes PEP8 incompliant code. This bear will not change
        functionality of the code in any way.

        :param max_line_length: Maximum number of characters for a line.
        :param tab_width:       Number of spaces per indent level.
        :param pep_ignore:      A list of errors/warnings to ignore.
        :param pep_select:      A list of errors/warnings to exclusively apply.
        """
        for result in self.retrieve_results(filename,
                                            file,
                                            pep_ignore=pep_ignore,
                                            pep_select=pep_select,
                                            max_line_length=max_line_length,
                                            indent_size=tab_width):
            yield result
