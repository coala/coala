import eradicate

from coalib.bearlib.abstractions.CorrectionBasedBear import CorrectionBasedBear


class PyCommentedCodeBear(CorrectionBasedBear):
    GET_REPLACEMENT = staticmethod(
        lambda file:
        (list(eradicate.filter_commented_out_code(''.join(file))), []))
    RESULT_MESSAGE = "This file contains commented out source code."

    def run(self, filename, file):
        """
        Detects commented out source code in Python.
        """
        for result in self.retrieve_results(filename, file):
            yield result
