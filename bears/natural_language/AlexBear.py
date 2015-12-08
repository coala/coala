import re

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear


class AlexBear(LocalBear, Lint):
    executable = 'alex'
    output_regex = re.compile(
        r'\s+(?P<line>\d+):(?P<column>\d+)\-'
        r'(?P<end_line>\d+):(?P<end_column>\d+)'
        r'\s+(?:(?P<warning>warning))\s+(?P<message>.+)')

    def run(self, filename, file):
        '''
        Checks the markdown file with Alex - Catch insensitive,
        inconsiderate writing.
        '''
        return self.lint(filename)
