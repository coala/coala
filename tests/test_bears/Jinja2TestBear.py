from coalib.bears.LocalBear import LocalBear


class Jinja2TestBear(LocalBear):
    LANGUAGES = {'jinja2'}
    LICENSE = 'AGPL-3.0'
    CAN_FIX = {'Formatting'}

    def run(self, filename, file, config: str = ''):
        """
        Bear to test that collecting of languages works.

        :param config: An optional dummy config file.
        """
