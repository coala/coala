import json

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear
from coalib.results.Diff import Diff
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.misc.Shell import escape_path_argument
from coalib.results.Result import Result


class ESLintBear(LocalBear, Lint):
    executable = 'eslint'
    arguments = '--no-ignore --no-color -f=json'
    severity_map = {
        "2": RESULT_SEVERITY.MAJOR,
        "1": RESULT_SEVERITY.NORMAL,
        "0": RESULT_SEVERITY.INFO
    }

    def run(self, filename, file, eslint_config: str=""):
        '''
        Checks the code with eslint. This will run eslint over each of the files
        seperately.

        :param eslint_config: The location of the .eslintrc config file.
        '''
        if eslint_config:
            self.arguments += (" --config "
                               + escape_path_argument(eslint_config))

        return self.lint(filename)

    def _process_issues(self, output, filename):
        try:
            output = json.loads("".join(output))
            lines = [line for line in open(filename)]
            lines = "".join(lines)
            newoutput = lines
            for lintLines in output[0]['messages']:
                if lintLines['severity'] == '0':
                    continue
                if 'fix' in lintLines:
                    fixStructure = lintLines['fix']
                    startingValue, endingValue = fixStructure['range']
                    replacementText = fixStructure['text']
                    newoutput = newoutput[
                        :int(startingValue)+1] + replacementText +\
                        newoutput[int(endingValue):]

            diff = Diff.from_string_arrays(
                lines.splitlines(True), newoutput.splitlines(True))

            yield Result.from_values(
                origin=self,
                message=lintLines['message'],
                file=filename,
                diffs={filename: diff},
                severity=self.severity_map[str(lintLines['severity'])],
                line=lintLines['line'])

        except:
            output = {}
