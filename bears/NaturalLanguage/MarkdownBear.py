from bears.linters.CorrectionBasedBear import CorrectionBasedBear


class MarkdownBear(CorrectionBasedBear):
    BINARY = 'mdast'
    RESULT_MESSAGE = "This markdown code does not comply to the set style."

    def run(self, filename, file):
        """
        Raises issues against style violations on markdown files.
        """
        cli = r'-s "bullet: \"*\", fences: true"'
        for result in self.retrieve_results(filename, file, cli_options=cli):
            yield result
