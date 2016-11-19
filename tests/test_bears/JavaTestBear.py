from coalib.bears.LocalBear import LocalBear


class JavaTestBear(LocalBear):
    LANGUAGES = {'java'}
    LICENSE = 'AGPL-3.0'

    def run(self, filename, file, config: str=''):
        """
        Bear to test that collecting of languages works.

        :param config: An optional dummy config file.
        """
