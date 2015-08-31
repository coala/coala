from coalib.bearlib.spacing.SpacingHelper import SpacingHelper
from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result
from coalib.misc.i18n import _


class LineLengthBear(LocalBear):
    def run(self,
            filename,
            file,
            max_line_length: int,
            tab_width: int=SpacingHelper.DEFAULT_TAB_WIDTH):
        '''
        Yields results for all lines longer than the given maximum line length.

        :param max_line_length: Maximum number of characters for a line.
        :param tab_width: Number of spaces to show for one tab.
        '''
        spacing_helper = SpacingHelper(tab_width)

        for line_number, line in enumerate(file):
            line = spacing_helper.replace_tabs_with_spaces(line)
            if len(line) > max_line_length + 1:
                yield Result(origin=self,
                             message=_("Line is longer than allowed.") +
                                     " ({actual} > {maximum})".format(
                                         actual=len(line),
                                         maximum=max_line_length),
                             file=filename,
                             line_nr=line_number + 1)
