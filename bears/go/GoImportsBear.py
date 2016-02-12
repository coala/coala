from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear


class GoImportsBear(Lint, LocalBear):
    executable = 'goimports'
    diff_message = "Imports need to be added/removed."
    use_stdin = True
    gives_corrected = True

    def run(self, filename, file):
        """
        Adds/Removes imports to Go code for missing imports.
        """
        return self.lint(filename, file)
