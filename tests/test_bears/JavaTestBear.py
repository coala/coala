from coalib.bears.LocalBear import LocalBear


class JavaTestBear(LocalBear):
    LANGUAGES = {'java'}

    def run(self, filename, file):
        """
        Bear to test that collecting of langugaes works.
        """
