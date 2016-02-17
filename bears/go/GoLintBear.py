import re

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear


class GoLintBear(LocalBear, Lint):
    executable = 'golint'
    output_regex = re.compile(
            r'(?P<path>.*?)\:(?P<line>\d+)\:(?P<column>\d+)\: (?P<message>.*)')
    use_stdout = True

    def run(self,
            filename,
            file,
            golint_cli_options: str=""):
        '''
        Checks the code using `golint`. This will run golint over each file
        seperately.

        :param golint_cli_options: Any other flags you wish to pass to golint
                                   can be passed.
        '''
        self.arguments = ""
        if golint_cli_options:
            self.arguments += " " + golint_cli_options
        self.arguments += " {filename}"

        return self.lint(filename)
