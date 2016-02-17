import re

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear


class GoVetBear(LocalBear, Lint):
    executable = 'go'
    arguments = 'vet {filename}'
    output_regex = re.compile(
        r'(?P<file_name>.+):(?P<line>\d+): (?P<message>.*)\n')
    use_stderr = True

    def run(self, filename, file):
        '''
        Checks the code using `go vet`.
        '''
        return self.lint(filename)
