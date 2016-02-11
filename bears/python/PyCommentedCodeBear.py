import eradicate

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear


class PyCommentedCodeBear(Lint, LocalBear):
    gives_corrected = True
    diff_message = "This file contains commented out source code."

    def lint(self, filename, file):
        output = list(eradicate.filter_commented_out_code(''.join(file)))
        return self.process_output(output, filename, file)

    def run(self, filename, file):
        """
        Detects commented out source code in Python.
        """
        return self.lint(filename, file)
