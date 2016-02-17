import re

from coalib.bearlib.spacing.SpacingHelper import SpacingHelper
from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result
from coalib.settings.Setting import typed_list


class LineLengthBear(LocalBear):

    def run(self,
            filename,
            file,
            max_line_length: int=80,
            tab_width: int=SpacingHelper.DEFAULT_TAB_WIDTH,
            ignore_length_regex: typed_list(str)=()):
        '''
        Yields results for all lines longer than the given maximum line length.

        :param max_line_length:     Maximum number of characters for a line.
        :param tab_width:           Number of spaces to show for one tab.
        :param ignore_length_regex: Lines matching each of the regular
                                    expressions in this list will be ignored.
        '''
        spacing_helper = SpacingHelper(tab_width)
        ignore_regexes = [re.compile(regex) for regex in ignore_length_regex]

        for line_number, line in enumerate(file):
            line = spacing_helper.replace_tabs_with_spaces(line)
            if len(line) > max_line_length + 1:
                if any(regex.search(line) for regex in ignore_regexes):
                    continue

                yield Result.from_values(
                    origin=self,
                    message="Line is longer than allowed." +
                            " ({actual} > {maximum})".format(
                                actual=len(line)-1,
                                maximum=max_line_length),
                    file=filename,
                    line=line_number + 1,
                    column=max_line_length + 1,
                    end_line=line_number + 1,
                    end_column=len(line))
