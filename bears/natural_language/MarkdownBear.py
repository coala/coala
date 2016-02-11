from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear


class MarkdownBear(Lint, LocalBear):
    executable = 'remark'
    diff_message = "The text does not comply to the set style."
    arguments = r'-s "bullet: \"*\", fences: true"'
    gives_corrected = True
    use_stdin = True

    def run(self, filename, file):
        """
        Raises issues against style violations on markdown files.
        """
        return self.lint(filename, file)
