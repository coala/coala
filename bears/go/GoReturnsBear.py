from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear


class GoReturnsBear(Lint, LocalBear):
    executable = 'goreturns'
    diff_message = "Imports or returns need to be added/removed."
    use_stdin = True
    gives_corrected = True

    def run(self, filename, file):
        """
        Proposes corrections of Go code using gofmt.
        """
        return self.lint(filename, file)
