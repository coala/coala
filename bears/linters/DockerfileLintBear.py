import json

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.results.Result import Result

class DockerfileLintBear(LocalBear, Lint):
    executable = 'dockerfile_lint'
    arguments = '--json -f'
    severity_map = {
        "error": RESULT_SEVERITY.MAJOR,
        "warn": RESULT_SEVERITY.NORMAL,
        "info": RESULT_SEVERITY.INFO}

    def run(self, filename, file):
        '''
        Checks the given file with dockerfile_lint.
        '''
        return self.lint(filename)

    def process_output(self, output, filename):
        output = json.loads(output)
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
