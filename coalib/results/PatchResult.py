"""
The PatchResult can be used to propose a change to the original code. To use the PatchResult you need to create a Diff
for each file you want to change and then pass those Diff's to the patch result.
"""
from coalib.results.Result import Result, RESULT_SEVERITY


class PatchResult(Result):
    def __init__(self, origin, message, diffs, file=None, severity=RESULT_SEVERITY.NORMAL):
        if not isinstance(diffs, dict):
            raise TypeError("diffs needs to be a dict.")
        Result.__init__(self, origin=origin, message=message, file=file, severity=severity)

        self.diffs = diffs

    def apply(self, file_dict):
        """
        Applies all contained diffs to the given file_dict. This operation will be done in-place.

        :param file_dict: A dictionary containing all files with filename as key and all lines a value. Will be
        modified.
        """
        if not isinstance(file_dict, dict):
            raise TypeError("file_dict needs to be a dict.")

        for filename in self.diffs:
            file_dict[filename] = self.diffs[filename].apply(file_dict[filename])
