import re

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear
from coalib.settings.Setting import typed_list


class CPPLintBear(LocalBear, Lint):
    executable = 'cpplint'
    output_regex = re.compile(
        r'(?P<filename>.+\..+):(?P<line>\d+):\s(?P<message>.+)')
    use_stderr = True

    def run(self,
            filename,
            file,
            max_line_length: int=80,
            cpplint_ignore: typed_list(str)=[],
            cpplint_include: typed_list(str)=[]):
        '''
        Checks the code with `cpplint` on each file separately.

        :param max_line_length: Maximum number of characters for a line.
        :param cpplint_ignore:  List of checkers to ignore.
        :param cpplint_include: List of checkers to explicitly enable.
        '''
        ignore = ','.join('-'+part.strip() for part in cpplint_ignore)
        include = ','.join('+'+part.strip() for part in cpplint_include)
        self.arguments = '--filter=' + ignore + ',' + include
        self.arguments += ' --linelength=' + str(max_line_length)
        self.arguments += ' {filename}'
        return self.lint(filename)
