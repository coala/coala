import uuid

from coalib.misc.Decorators import (generate_repr,
                                    generate_ordering,
                                    enforce_signature)
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


@generate_repr("id",
               "origin",
               "file",
               "line_nr",
               ("severity", RESULT_SEVERITY.reverse.get),
               "message")
@generate_ordering("file",
                   "line_nr",
                   "severity",
                   "origin",
                   "message",
                   "debug_msg",
                   "diffs")
class Result:
    """
    A result is anything that has an origin and a message.

    Optionally it might affect a file.
    """

    @enforce_signature
    def __init__(self,
                 origin,
                 message: str,
                 file: (str, None)=None,
                 line_nr: (int, None)=None,
                 severity: int=RESULT_SEVERITY.NORMAL,
                 debug_msg="",
                 diffs: (dict, None)=None):
        """
        :param origin:    Class name or class of the creator of this object
        :param message:   Message to show with this result
        :param file:      The path to the affected file
        :param line_nr:   Number of the line which is affected, first line is 1
        :param severity:  Severity of this result
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
        self.id = uuid.uuid4().int

    def to_string_dict(self):
        """
        Makes a dictionary which has all keys and values as strings and
        contains all the data that the base Result has.

        FIXME: diffs are not serialized ATM.

        :return: Dictionary with keys and values as string.
        """
        retval = {}

        members = ["id",
                   "debug_msg",
                   "file",
                   "line_nr",
                   "message",
                   "origin"]

        for member in members:
            value = getattr(self, member)
            retval[member] = "" if value == None else str(value)

        retval["severity"] = str(RESULT_SEVERITY.reverse.get(self.severity, ""))

        return retval

    @enforce_signature
    def apply(self, file_dict: dict):
        """
        Applies all contained diffs to the given file_dict. This operation will
        be done in-place.

        :param file_dict: A dictionary containing all files with filename as
                          key and all lines a value. Will be modified.
        """
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
