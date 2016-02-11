import autoflake

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear


class PyUnusedCodeBear(Lint, LocalBear):
    diff_message = "This file contains unused source code."
    gives_corrected = True

    def lint(self, filename, file):
        output = autoflake.fix_code(''.join(file)).splitlines(True)
        return self.process_output(output, filename, file)

    def run(self, filename, file):
        """
        Detects unused code. This functionality is limited to:

        - Unneeded pass statements.
        - Unneeded builtin imports. (Others might have side effects.)
        """
        return self.lint(filename, file)
