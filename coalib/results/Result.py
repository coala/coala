from functools import total_ordering

from coalib.misc.Decorators import generate_repr
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


@generate_repr("origin",
               "file",
               "line_nr",
               ("severity", RESULT_SEVERITY.reverse.get),
               "message")
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
                 debug_msg="",
                 diffs=None):
        """
        :param origin:    Class name or class of the creator of this object
        :param message:   Message to show with this result
        :param file:      The path to the affected file
        :param severity:  Severity of this result
        :param line_nr:   Number of the line which is affected, first line is 1
        :param debug_msg: A message which may help the user find out why
                          this result was yielded.
        :param diffs:     A dictionary associating a Diff object with each
                          filename.
        """
        origin = origin or ""
        if not isinstance(origin, str):
            origin = origin.__class__.__name__

        self.origin = origin
        self.message = message
        self.debug_msg = debug_msg
        self.file = file
        self.line_nr = line_nr
        self.severity = severity
        self.diffs = diffs

    def __str__(self):
        return ("Result:\n origin: {origin}\n file: {file}\n line nr: "
                "{linenr}\n severity: {severity}\n diffs: {diffs}\n{msg}"
                .format(origin=repr(self.origin),
                        file=repr(self.file),
                        linenr=self.line_nr,
                        severity=self.severity,
                        diffs=repr(self.diffs),
                        msg=repr(self.message)))

    def __eq__(self, other):
        return (isinstance(other, Result) and
                self.origin == other.origin and
                self.message == other.message and
                self.debug_msg == other.debug_msg and
                self.file == other.file and
                self.severity == other.severity and
                self.line_nr == other.line_nr and
                self.diffs == other.diffs)

    def __lt__(self, other):
        if not isinstance(other, Result):
            raise TypeError("Comparison with non-result classes is not "
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

    def to_string_dict(self):
        """
        Makes a dictionary which has all keys and values as strings and
        contains all the data that the base Result has.

        FIXME: diffs are not serialized ATM.

        :return: Dictionary with keys and values as string.
        """
        retval = {}

        members = ["debug_msg",
                   "file",
                   "line_nr",
                   "message",
                   "origin"]

        for member in members:
            value = getattr(self, member)
            retval[member] = "" if value == None else str(value)

        retval["severity"] = str(RESULT_SEVERITY.reverse.get(self.severity, ""))

        return retval

    def apply(self, file_dict):
        """
        Applies all contained diffs to the given file_dict. This operation will
        be done in-place.

        :param file_dict: A dictionary containing all files with filename as
                          key and all lines a value. Will be modified.
        """
        assert isinstance(file_dict, dict)
        assert isinstance(self.diffs, dict)

        for filename in self.diffs:
            file_dict[filename] = self.diffs[filename].apply(
                file_dict[filename])

    def __add__(self, other):
        """
        Joins those patches to one patch.

        :param other: The other patch.
        """
        assert isinstance(self.diffs, dict)
        assert isinstance(other.diffs, dict)

        for filename in other.diffs:
            if filename in self.diffs:
                self.diffs[filename] += other.diffs[filename]
            else:
                self.diffs[filename] = other.diffs[filename]

        return self
