import eradicate

from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result
from coalib.results.Diff import Diff
from coalib.misc.i18n import _


class PyCommentedCodeBear(LocalBear):
    def run(self, filename, file):
        """
        Detects commented out source code in Python.
        """
        content = ''.join(file)
        new_content = list(eradicate.filter_commented_out_code(content))
        if new_content != file:
            diff = Diff.from_string_arrays(file, new_content)

            yield Result(
                self,
                _("This file contains commented out source code."),
                affected_code=diff.affected_code(filename),
                diffs={filename: diff})
