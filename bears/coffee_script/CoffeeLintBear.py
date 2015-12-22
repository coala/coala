from io import StringIO
from csv import DictReader

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.results.Result import Result


def convert_if_not_empty(value: str, conversion):
    """
    Returns the value converted if it is not None or empty.

    :param value:      The value to convert.
    :param conversion: The conversion callable.
    :return:           None or the converted value.
    """
    if value is not None and value != '':
        return conversion(value)

    return None


class CoffeeLintBear(LocalBear, Lint):
    executable = 'coffeelint'
    arguments = '--reporter=csv'
    severity_map = {'warn': RESULT_SEVERITY.NORMAL,
                    'error': RESULT_SEVERITY.MAJOR}

    def run(self, filename, file):
        """
        Coffeelint's your files!
        """
        return self.lint(filename)

    def process_output(self, output, filename):
        reader = DictReader(StringIO(output))

        for row in reader:
            try:
                yield Result.from_values(
                    origin=self,
                    message=row['message'],
                    file=filename,
                    line=convert_if_not_empty(row['lineNumber'], int),
                    end_line=convert_if_not_empty(row['lineNumberEnd'], int),
                    severity=self.severity_map[row['level']])
            except KeyError:  # Invalid CSV line, ignore
                pass
