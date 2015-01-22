from coalib.bearlib.spacing.SpacingHelper import SpacingHelper
from coalib.bears.results.LineResult import LineResult
from coalib.bears.LocalBear import LocalBear


class SpaceConsistencyBear(LocalBear):
    def run_bear(self,
                 filename,
                 file,
                 use_spaces: bool,
                 allow_trailing_whitespace: bool=False,
                 tab_width: int=SpacingHelper.DEFAULT_TAB_WIDTH):
        """
        Checks the space consistency for each line.

        :param use_spaces: True if spaces are to be used instead of tabs.
        :param allow_trailing_whitespace: Whether to allow trailing whitespace or not.
        :param tab_width: Number of spaces representing one tab.
        """
        results = []
        filtername = self.__class__.__name__

        spacing_helper = SpacingHelper(tab_width)

        for line_number, line in enumerate(file):
            if not allow_trailing_whitespace:
                replacement = line.rstrip(" \t\n") + "\n"
                if replacement != line:
                    results.append(LineResult(filtername,
                                              line_number+1,
                                              line,
                                              self._("Line has trailing whitespace characters"),
                                              filename))
                    line = replacement

            if use_spaces:
                replacement = spacing_helper.replace_tabs_with_spaces(line)
                if replacement != line:
                    results.append(LineResult(filtername,
                                              line_number+1,
                                              line,
                                              self._("Line contains one or more tabs"),
                                              filename))
            else:
                replacement = spacing_helper.replace_spaces_with_tabs(line)
                if replacement != line:
                    results.append(LineResult(filtername,
                                              line_number+1,
                                              line,
                                              self._("Line contains with tab replaceable spaces"),
                                              filename))

        return results
