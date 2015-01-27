from coalib.bearlib.spacing.SpacingHelper import SpacingHelper
from coalib.bears.LocalBear import LocalBear
from coalib.results.LineResult import LineResult
from coalib.misc.i18n import _


class LineLengthBear(LocalBear):
    def run_bear(self,
                 filename,
                 file,
                 max_line_length: int,
                 tab_width: int=SpacingHelper.DEFAULT_TAB_WIDTH):
        """
        Yields results for all lines longer than the given maximum line length.

        :param max_line_length: Maximum number of characters for a line.
        :param tab_width: Number of spaces to show for one tab.
        """
        results = []
        bearname = self.__class__.__name__
        spacing_helper = SpacingHelper.from_section(section=self.section)

        for line_number, line in enumerate(file):
            line = spacing_helper.replace_tabs_with_spaces(line)
            if len(line) > max_line_length + 1:
                results.append(LineResult(bearname,
                                          line_number + 1,
                                          line,
                                          _("Line is longer than allowed.") +
                                          " ({actual} > {maximum})".format(actual=len(line), maximum=max_line_length),
                                          filename))

        return results
