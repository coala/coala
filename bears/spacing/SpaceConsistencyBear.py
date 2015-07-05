from coalib.bearlib.spacing.SpacingHelper import SpacingHelper
from coalib.results.Diff import Diff
from coalib.bears.LocalBear import LocalBear
from coalib.misc.i18n import _
from coalib.results.PatchResult import PatchResult


class SpaceConsistencyBear(LocalBear):
    def run(self,
            filename,
            file,
            use_spaces: bool,
            allow_trailing_whitespace: bool=False,
            tab_width: int=SpacingHelper.DEFAULT_TAB_WIDTH):
        '''
        Checks the space consistency for each line.

        :param use_spaces:                True if spaces are to be used
                                          instead of tabs.
        :param allow_trailing_whitespace: Whether to allow trailing whitespace
                                          or not.
        :param tab_width:                 Number of spaces representing one
                                          tab.
        '''
        spacing_helper = SpacingHelper(tab_width)

        for line_number, line in enumerate(file):
            replacement = line

            if not allow_trailing_whitespace:
                replacement = replacement.rstrip(" \t\n") + "\n"

            if use_spaces:
                replacement = spacing_helper.replace_tabs_with_spaces(
                    replacement)
            else:
                replacement = spacing_helper.replace_spaces_with_tabs(
                    replacement)

            if replacement != line:
                diff = Diff()
                diff.change_line(line_number + 1, line, replacement)
                yield PatchResult(self,
                                  _("Line contains spacing inconsistencies."),
                                  {filename: diff},
                                  filename,
                                  line_nr=line_number+1)
