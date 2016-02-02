from coalib.bearlib.abstractions.CorrectionBasedBear import CorrectionBasedBear


class GofmtBear(CorrectionBasedBear):
    executable = 'gofmt'
    RESULT_MESSAGE = "Formatting can be improved."

    def run(self, filename, file):
        """
        Proposes corrections of Go code using gofmt.
        """
        for result in self.retrieve_results(filename, file, cli_options=''):
            yield result
