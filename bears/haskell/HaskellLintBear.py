import json

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result
from coalib.results.Diff import Diff
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


class HaskellLintBear(LocalBear, Lint):
    executable = 'hlint'
    arguments = '--json {filename}'
    severity_map = {
        "Error": RESULT_SEVERITY.MAJOR,
        "Warning": RESULT_SEVERITY.NORMAL,
        "Suggestion": RESULT_SEVERITY.INFO}
    gives_corrected = True

    def run(self, filename, file):
        '''
        Checks the given file with hlint.
        '''
        return self.lint(filename=filename, file=file)

    def _process_corrected(self, output, filename, file):
        output = json.loads("".join(output))

        for issue in output:
            diff = Diff(file)
            line_nr = issue["startLine"]
            line_to_change = file[line_nr-1]
            newline = line_to_change.replace(issue["from"], issue["to"])
            diff.change_line(line_nr, line_to_change, newline)

            yield Result.from_values(
                origin=self,
                message=issue["hint"],
                file=filename,
                severity=self.severity_map[issue["severity"]],
                line=issue["startLine"],
                diffs={filename: diff})
