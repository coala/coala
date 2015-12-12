import re

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear


class ProseLintBear(LocalBear, Lint):
    executable = 'proselint'
    output_regex = re.compile(
        r'.+?:(?P<line>\d+):(?P<column>\d+): (?P<code>\S*) (?P<message>.+)')

    def run(self, filename, file):
        '''
        Checks the markdown file with Alex - Catch insensitive,
        inconsiderate writing.
        '''
        return self.lint(filename)
