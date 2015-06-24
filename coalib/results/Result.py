from functools import total_ordering

from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.results.result_actions.OpenEditorAction import OpenEditorAction


@total_ordering
class Result:
    """
    A result is anything that has an origin and a message.

    Optionally it might affect a file.

    When sorting a list of results with the implemented comparision routines
    you will get an ordering which follows the following conditions,
    while the first condition has the highest priority, which descends to the
    last condition.
    1. Results with no files will be shown first
    2. Results will be sorted by files (ascending alphabetically)
    3. Results will be sorted by lines (ascending)
    4. Results will be sorted by severity (descending, major first, info last)
    5. Results will be sorted by origin (ascending alphabetically)
    6. Results will be sorted by message (ascending alphabetically)
    7. Results will be sorted by debug message (ascending alphabetically)
    """

    def __init__(self,
                 origin,
                 message,
                 file=None,
                 severity=RESULT_SEVERITY.NORMAL,
                 line_nr=None,
                 debug_msg=""):
        """
        :param origin:    Class name or class of the creator of this object
        :param message:   Message to show with this result
        :param file:      The path to the affected file
        :param severity:  Severity of this result
        :param line_nr:   Number of the line which is affected, first line is 1
        :param debug_msg: A message which may help the user find out why
                          this result was yielded.
        """
        if not isinstance(origin, str):
            origin = origin.__class__.__name__

        self.origin = origin
        self.message = message
        self.debug_msg = debug_msg
        self.file = file
        self.line_nr = line_nr
        self.severity = severity

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "Result:\n origin: '{origin}'\n file: '{file}'\n line nr: " \
               "{linenr}\n severity: {severity}\n" \
               "'{msg}'".format(origin=self.origin,
                                file=self.file,
                                severity=self.severity,
                                msg=self.message,
                                linenr=self.line_nr)

    def __eq__(self, other):
        return (isinstance(other, Result) and
                self.origin == other.origin and
                self.message == other.message and
                self.debug_msg == other.debug_msg and
                self.file == other.file and
                self.severity == other.severity and
                self.line_nr == other.line_nr)

    def __lt__(self, other):
        if not isinstance(other, Result):
            raise TypeError("Comparision with non-result classes is not "
                            "supported.")

        # Show elements without files first
        if (self.file is None) != (other.file is None):
            return self.file is None

        # Now either both .file members are None or both are set
        if self.file != other.file:
            return self.file < other.file

        # If we have a line result show results with a lesser line number first
        if self.line_nr is not None and other.line_nr is not None:
            if self.line_nr != other.line_nr:
                return self.line_nr < other.line_nr

        # Both files are equal
        if self.severity != other.severity:
            return self.severity > other.severity

        # Severities are equal, files are equal
        if self.origin != other.origin:
            return self.origin < other.origin

        if self.message != other.message:
            return self.message < other.message

        return self.debug_msg < other.debug_msg

    def get_actions(self):
        """
        :return: All ResultAction classes applicable to this result.
        """
        actions = []
        if self.file is not None:
            actions.append(OpenEditorAction())

        return actions
