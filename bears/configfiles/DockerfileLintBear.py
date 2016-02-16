import json

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


class DockerfileLintBear(LocalBear, Lint):
    executable = 'dockerfile_lint'
    arguments = '--json -f {filename}'
    severity_map = {
        "error": RESULT_SEVERITY.MAJOR,
        "warn": RESULT_SEVERITY.NORMAL,
        "info": RESULT_SEVERITY.INFO}

    def run(self, filename, file):
        '''
        Checks the given file with dockerfile_lint.
        '''
        return self.lint(filename)

    def _process_issues(self, output, filename):
        output = json.loads("".join(output))

        for severity in output:
            if severity == "summary":
                continue
            for issue in output[severity]["data"]:
                yield Result.from_values(
                    origin=self,
                    message=issue["message"],
                    file=filename,
                    severity=self.severity_map[issue["level"]],
                    line=issue["line"])
