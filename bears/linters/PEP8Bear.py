import autopep8

from bears.linters.CorrectionBasedBear import CorrectionBasedBear


class PEP8Bear(CorrectionBasedBear):
    GET_REPLACEMENT = staticmethod(
        lambda file: (autopep8.fix_code(''.join(file)).splitlines(True), []))
    RESULT_MESSAGE = "The code does not comply to PEP8."

    def run(self, filename, file):
        """
        Detects and fixes PEP8 incompliant code. This bear will not change
        functionality of the code in any way.
        """
        for result in self.retrieve_results(filename, file):
            yield result
