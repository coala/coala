from isort import SortImports

from coalib.bears.LocalBear import LocalBear
from coalib.results.Diff import Diff
from coalib.results.Result import Result


class PyImportSortBear(LocalBear):

    def run(self, filename, file):
        """
        Sorts imports for python.
        """
        new_file = SortImports(
            file_contents=''.join(file)).output.splitlines(True)
        if new_file != file:
            diff = Diff.from_string_arrays(file, new_file)
            yield Result(self,
                         "Imports can be sorted.",
                         affected_code=diff.affected_code(filename),
                         diffs={filename: diff})
