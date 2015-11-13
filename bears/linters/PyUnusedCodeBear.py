import autoflake

from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result
from coalib.results.Diff import Diff
from coalib.misc.i18n import _


class PyUnusedCodeBear(LocalBear):
    def run(self, filename, file):
        """
        Detects unused code. This functionality is limited to:

        - Unneeded pass statements.
        - Unneeded builtin imports. (Others might have side effects.)
        """
        content = ''.join(file)
        new_content = autoflake.fix_code(content)
        if new_content != content:
            diff = Diff.from_string_arrays(file, new_content.splitlines(True))

            yield Result(
                self,
                _("This file contains unused source code."),
                affected_code=diff.affected_code(filename),
                diffs={filename: diff})
