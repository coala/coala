from isort import SortImports

from coalib.bearlib.spacing.SpacingHelper import SpacingHelper
from coalib.bears.LocalBear import LocalBear
from coalib.results.Diff import Diff
from coalib.results.Result import Result


class PyImportSortBear(LocalBear):

    def run(self,
            filename,
            file,
            use_spaces: bool=True,
            tab_width: int=SpacingHelper.DEFAULT_TAB_WIDTH,
            max_line_length: int=80,
            use_parentheses_in_import: bool=True,
            sort_imports_by_length: bool=False,
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
        :param sort_imports_by_length:    Set to true to sort imports by length
                                          instead of alphabetically.
        :param isort_multi_line_output:   The type of formatting to be used by
                                          isort when indenting imports. This
                                          value if passed to isort as the
                                          `multi_line_output` setting.
        """
        indent = "Tab" if use_spaces == False else tab_width
        new_file = tuple(SortImports(
            file_contents=''.join(file),
            line_length=max_line_length,
            indent=indent,
            multi_line_output=isort_multi_line_output,
            use_parentheses=use_parentheses_in_import,
            length_sort=sort_imports_by_length).output.splitlines(True))

        if new_file != tuple(file):
            diff = Diff.from_string_arrays(file, new_file)
            yield Result(self,
                         "Imports can be sorted.",
                         affected_code=diff.affected_code(filename),
                         diffs={filename: diff})
