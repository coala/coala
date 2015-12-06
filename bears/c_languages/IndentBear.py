import platform
from bears.linters.CorrectionBasedBear import CorrectionBasedBear


class IndentBear(CorrectionBasedBear):
    BINARY = "indent" if platform.system() != "Darwin" else "gindent"
    RESULT_MESSAGE = "Indentation can be improved."

    def run(self,
            filename,
            file,
            indent_cli_options: str='--k-and-r-style'):
        """
        This bear checks and corrects spacing and indentation via the well
        known Indent utility. It is designed to work with the C programming
        language but may work reasonably with syntactically similar languages.

        :param indent_cli_options: Any command line options the indent binary
                                   understands. They will be simply passed
                                   through.
        """
        for result in self.retrieve_results(filename,
                                            file,
                                            cli_options=indent_cli_options):
            yield result
