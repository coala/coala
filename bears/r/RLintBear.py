import re
import shutil
import subprocess
import os

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


class RLintBear(LocalBear, Lint):
    executable = 'Rscript'
    arguments = " -e 'library(lintr)' -e 'lint({filename})'"
    output_regex = re.compile(
        r'(?P<file_name>\S+):(?P<line>\S+):(?P<col>\S+):'
        r' (?P<severity>\S+): (?P<message>.*)')
    severity_map = {
        "warning": RESULT_SEVERITY.NORMAL,
        "error": RESULT_SEVERITY.MAJOR,
        "style": RESULT_SEVERITY.NORMAL}

    @classmethod
    def check_prerequisites(cls):
        if shutil.which("Rscript") is None:
            return "R is not installed."
        else:
            try:
                FNULL = open(os.devnull, 'w')
                subprocess.check_call(
                    ["Rscript", "-e", "library(lintr)"],
                     stdout=FNULL, stderr=subprocess.STDOUT)
                return True
            except subprocess.CalledProcessError:
                return 'Package lintr is not installed.'

    def run(self, filename, file):
        '''
        Checks the code with `lintr`.
        '''
        return self.lint(filename)
