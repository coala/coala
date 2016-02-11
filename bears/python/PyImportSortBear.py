from isort import SortImports

from coalib.bearlib.abstractions.CorrectionBasedBear import CorrectionBasedBear
from coalib.bearlib.spacing.SpacingHelper import SpacingHelper


class PyImportSortBear(CorrectionBasedBear):
    RESULT_MESSAGE = "Imports can be sorted."

    @staticmethod
    def run_isort(file,
                  use_spaces,
                  max_line_length,
                  indent_size,
                  use_parentheses_in_import,
                  isort_multi_line_output):
        indent = "Tab" if use_spaces == False else indent_size
        new_file = SortImports(file_contents=''.join(file),
                               line_length=max_line_length,
                               indent=indent,
                               multi_line_output=isort_multi_line_output,
                               use_parentheses=use_parentheses_in_import).output
        return new_file.splitlines(True), []

    GET_REPLACEMENT = run_isort

    def run(self,
            filename,
            file,
            use_spaces: bool=True,
            tab_width: int=SpacingHelper.DEFAULT_TAB_WIDTH,
            max_line_length: int=80,
            use_parentheses_in_import: bool=True,
            isort_multi_line_output: int=4):
        """
        Sorts imports for python.

        :param use_spaces:                True if spaces are to be used
                                          instead of tabs.
        :param tab_width:                 Number of spaces per indent level.
        :param max_line_length:           Maximum number of characters for
                                          a line.
        :param use_parentheses_in_import: True if parenthesis are to be used
                                          in import statements.
        :param isort_multi_line_output:   The type of formatting to be used by
                                          isort when indenting imports. This
                                          value if passed to isort as the
                                          `multi_line_output` setting.
        """
        for result in self.retrieve_results(
                  filename,
                  file,
                  use_spaces=use_spaces,
                  indent_size=tab_width,
                  max_line_length=max_line_length,
                  use_parentheses_in_import=use_parentheses_in_import,
                  isort_multi_line_output=isort_multi_line_output):
            yield result
