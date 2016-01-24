import platform

from coalib.bearlib.abstractions.CorrectionBasedBear import CorrectionBasedBear
from coalib.bearlib.spacing.SpacingHelper import SpacingHelper


class IndentBear(CorrectionBasedBear):
    executable = "indent" if platform.system() != "Darwin" else "gindent"
    RESULT_MESSAGE = "Indentation can be improved."

    def run(self,
            filename,
            file,
            max_line_length: int=80,
            use_spaces: bool=True,
            tab_width: int=SpacingHelper.DEFAULT_TAB_WIDTH,
            indent_cli_options: str=''):
        """
        This bear checks and corrects spacing and indentation via the well
        known Indent utility. It is designed to work with the C programming
        language but may work reasonably with syntactically similar languages.

        :param max_line_length:    Maximum number of characters for a line.
        :param use_spaces:         True if spaces are to be used, else tabs.
        :param tab_width:          Number of spaces per indent level.
        :param indent_cli_options: Any command line options the indent binary
                                   understands. They will be simply passed
                                   through.
        """
        options = "--no-tabs" if use_spaces else "--use-tabs"
        options += (" --line-length {0} --indent-level {1} --tab-size {1} "
                    "{2}".format(max_line_length,
                                 tab_width,
                                 indent_cli_options))
        for result in self.retrieve_results(filename,
                                            file,
                                            cli_options=options):
            yield result
