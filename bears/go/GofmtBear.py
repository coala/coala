from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear


class GofmtBear(Lint, LocalBear):
    executable = 'gofmt'
    diff_message = "Formatting can be improved."
    use_stdin = True
    gives_corrected = True

    def run(self, filename, file):
        """
        Proposes corrections of Go code using gofmt.
        """
        return self.lint(filename, file)
