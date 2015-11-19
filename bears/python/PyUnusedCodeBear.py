import autoflake

from bears.linters.CorrectionBasedBear import CorrectionBasedBear


class PyUnusedCodeBear(CorrectionBasedBear):
    GET_REPLACEMENT = staticmethod(
        lambda file: (autoflake.fix_code(''.join(file)).splitlines(True), []))
    RESULT_MESSAGE = "This file contains unused source code."

    def run(self, filename, file):
        """
        Detects unused code. This functionality is limited to:

        - Unneeded pass statements.
        - Unneeded builtin imports. (Others might have side effects.)
        """
        for result in self.retrieve_results(filename, file):
            yield result
