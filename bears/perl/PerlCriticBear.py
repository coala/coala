import re

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear
from coalib.misc.Shell import escape_path_argument
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


class PerlCriticBear(LocalBear, Lint):
    executable = 'perlcritic'
    output_regex = re.compile(
            r'(?P<line>\d+)\|(?P<column>\d+)\|(?P<severity>\d+)\|'
            r'(?P<origin>.*?)\|(?P<message>.*)')
    severity_map = {
        "1": RESULT_SEVERITY.MAJOR,
        "2": RESULT_SEVERITY.MAJOR,
        "3": RESULT_SEVERITY.NORMAL,
        "4": RESULT_SEVERITY.NORMAL,
        "5": RESULT_SEVERITY.INFO}

    def run(self,
            filename,
            file,
            perlcritic_config: str=""):
        '''
        Checks the code with perlcritic. This will run perlcritic over
        each of the files seperately

        :param perlcritic_config: Location of the perlcriticrc config file.
        '''
        self.arguments = '--no-color --verbose "%l|%c|%s|%p|%m (%e)"'
        if perlcritic_config:
            self.arguments += (" --config "
                               + escape_path_argument(perlcritic_config))
        self.arguments += " {filename}"
        return self.lint(filename)
