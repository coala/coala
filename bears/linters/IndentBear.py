from subprocess import Popen, PIPE
import platform

from coalib.bears.LocalBear import LocalBear
from coalib.results.Diff import Diff
from coalib.results.Result import Result


INDENT_BINARY = "indent" if platform.system() != "Darwin" else "gindent"


class IndentBear(LocalBear):
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
        process = Popen(INDENT_BINARY + " " + indent_cli_options,
                        shell=True,
                        stdin=PIPE,
                        stdout=PIPE,
                        stderr=PIPE,
                        universal_newlines=True)
        process.stdin.writelines(file)
        process.stdin.close()
        process.wait()
        new_file = process.stdout.readlines()
        if new_file != file:
            wholediff = Diff.from_string_arrays(file, new_file)

            for diff in wholediff.split_diff():
                yield Result(
                    self,
                    "Spacing does not comply to the given standards.",
                    affected_code=(diff.range(filename),),
                    diffs={filename: diff})

        process.stdout.close()
        process.stderr.close()
