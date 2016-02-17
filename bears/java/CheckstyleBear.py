from os.path import abspath, dirname, join
import re
import shutil
import subprocess

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


class CheckstyleBear(LocalBear, Lint):
    executable = 'java'
    google_checks = join(dirname(abspath(__file__)), 'google_checks.xml')
    jar = join(dirname(abspath(__file__)), 'checkstyle.jar')

    severity_map = {
        "INFO": RESULT_SEVERITY.INFO,
        "WARN": RESULT_SEVERITY.NORMAL}

    @classmethod
    def check_prerequisites(cls):  # pragma: no cover
        if shutil.which("java") is None:
            return "java is not installed."
        else:
            exitcode = subprocess.call(["java", "-jar", cls.jar, "-v"])
            if exitcode != 0:
                return ("jar file {} is invalid and cannot be used"
                        .format(cls.jar))
            else:
                return True

    def run(self, filename, file):
        """
        Checks the code using `checkstyle` using the Google codestyle
        specification.
        """
        self.output_regex = re.compile(
            r'\[(?P<severity>WARN|INFO)\]\s*' + re.escape(abspath(filename)) +
            r':(?P<line>\d+)(:(?P<col>\d+))?:\s*'
            r'(?P<message>.*?)\s*\[(?P<origin>[a-zA-Z]+?)\]')
        self.arguments = '-jar ' + self.jar + ' -c ' + self.google_checks
        self.arguments += " {filename}"
        return self.lint(filename)
