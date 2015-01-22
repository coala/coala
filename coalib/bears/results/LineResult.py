from coalib.bears.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.bears.results.Result import Result


class LineResult(Result):
    """
    This is a result that affects one specific line in a file.
    """

    def __init__(self, origin, line_nr, line, message, file, severity=RESULT_SEVERITY.NORMAL):
        Result.__init__(self, origin=origin, message=message, file=file, severity=severity)
        self.line_nr = line_nr
        self.line = line

    def __str__(self):
        return "LineResult:\n origin: '{origin}'\n file: '{file}'\n severity: {severity}\n line: '{line}'\n line nr: " \
               "{linenr}\n'{msg}'".format(origin=self.origin, file=self.file, severity=self.severity, msg=self.message,
                                          line=self.line, linenr=self.line_nr)

    # Result's __ne__ uses __eq__ so no need to overwrite that too
    def __eq__(self, other):
        return Result.__eq__(self, other) and \
               isinstance(other, LineResult) and \
               self.line_nr == other.line_nr and \
               self.line == other.line
