import eradicate

from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result
from coalib.results.Diff import Diff


class PyCommentedCodeBear(LocalBear):
    def run(self, filename, file):
        """
        Detects commented out source code in Python.
        """
        content = ''.join(file)
        new_content = list(eradicate.filter_commented_out_code(content))
        if new_content != file:
            wholediff = Diff.from_string_arrays(file, new_content)
            for diff in wholediff.split_diff():
                yield Result(
                    self,
                    "This file contains commented out source code.",
                    affected_code=(diff.range(filename),),
                    diffs={filename: diff})
