from coalib.bears.LocalBear import LocalBear
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.results.Result import Result
from coalib.results.Diff import Diff
from coalib.bearlib.parsing.clang.cindex import Index
from coalib.results.SourceRange import SourceRange


class ClangBear(LocalBear):
    def run(self, filename, file):
        """
        Runs Clang over the given files and raises/fixes any upcoming issues.
        """
        index = Index.create()
        diagnostics = index.parse(
            filename,
            unsaved_files=[(filename.encode(),
                            ''.join(file).encode())]).diagnostics
        for diag in diagnostics:
            severity = {0: RESULT_SEVERITY.INFO,
                        1: RESULT_SEVERITY.INFO,
                        2: RESULT_SEVERITY.NORMAL,
                        3: RESULT_SEVERITY.MAJOR,
                        4: RESULT_SEVERITY.MAJOR}.get(diag.severity)
            affected_code = tuple(SourceRange.from_clang_range(range)
                                  for range in diag.ranges)

            diffs = None
            fixits = list(diag.fixits)
            if len(fixits) > 0:
                # FIXME: coala doesn't support choice of diffs, for now
                # append first one only, often there's only one anyway
                diffs = {filename: Diff.from_clang_fixit(fixits[0], file)}

                # If clang ships no range, take the stuff related to diff
                if len(affected_code) == 0:
                    affected_code = diffs[filename].affected_code(filename)

            yield Result(
                self,
                diag.spelling.decode(),
                severity=severity,
                affected_code=affected_code,
                diffs=diffs)
