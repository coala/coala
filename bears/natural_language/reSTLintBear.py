from restructuredtext_lint import lint

from coalib.bears.LocalBear import LocalBear
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.results.Result import Result


class reSTLintBear(LocalBear):
    def run(self, filename, file):
        """
        Lints reStructuredText.
        """
        content = ''.join(file)
        errors = lint(content)

        for error in errors:
            severity = {
                1: RESULT_SEVERITY.INFO,
                2: RESULT_SEVERITY.NORMAL,
                3: RESULT_SEVERITY.MAJOR,
                4: RESULT_SEVERITY.MAJOR}.get(error.level,
                                              RESULT_SEVERITY.NORMAL)
            yield Result.from_values(
                self,
                error.message,
                file=filename,
                line=error.line,
                debug_msg=error.full_message,
                severity=severity)
