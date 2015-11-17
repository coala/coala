import autopep8

from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result
from coalib.results.Diff import Diff
from coalib.misc.i18n import _


class PEP8Bear(LocalBear):
    def run(self, filename, file):
        """
        Detects and fixes PEP8 incompliant code. This bear will not change
        functionality of the code in any way.
        """
        content = ''.join(file)
        new_content = autopep8.fix_code(content)
        if new_content != content:
            wholediff = Diff.from_string_arrays(file,
                                                new_content.splitlines(True))
            for diff in wholediff.split_diff():
                yield Result(
                    self,
                    _("The code does not comply to PEP8."),
                    affected_code=(diff.range(filename),),
                    diffs={filename: diff})
