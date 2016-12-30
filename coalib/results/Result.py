import uuid
from os.path import relpath

from coala_utils.decorators import (
    enforce_signature, generate_ordering, generate_repr, get_public_members)
from coalib.bearlib.aspects import aspectbase
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.results.SourceRange import SourceRange


# Omit additional info, debug message and diffs for brevity
@generate_repr(('id', hex),
               'origin',
               'affected_code',
               ('severity', RESULT_SEVERITY.reverse.get),
               'confidence',
               'message',
               ('aspect', lambda aspect: type(aspect).__qualname__))
@generate_ordering('affected_code',
                   'severity',
                   'confidence',
                   'origin',
                   'message',
                   'aspect',
                   'additional_info',
                   'debug_msg')
class Result:
    """
    A result is anything that has an origin and a message.

    Optionally it might affect a file.
    """

    @enforce_signature
    def __init__(self,
                 origin,
                 message: str,
                 affected_code: (tuple, list)=(),
                 severity: int=RESULT_SEVERITY.NORMAL,
                 additional_info: str='',
                 debug_msg='',
                 diffs: (dict, None)=None,
                 confidence: int=100,
                 aspect: (aspectbase, None)=None):
        """
        :param origin:
            Class name or creator object of this object.
        :param message:
            Message to show with this result.
        :param affected_code:
            A tuple of SourceRange objects pointing to related positions in the
            source code.
        :param severity:
            Severity of this result.
        :param additional_info:
            A long description holding additional information about the issue
            and/or how to fix it. You can use this like a manual entry for a
            category of issues.
        :param debug_msg:
            A message which may help the user find out why this result was
            yielded.
        :param diffs:
            A dictionary with filename as key and ``Diff`` object
            associated with it as value.
        :param confidence:
            A number between 0 and 100 describing the likelihood of this result
            being a real issue.
        :param aspect:
            An aspectclass instance which this result is associated to.
            Note that this should be a leaf of the aspect tree!
            (If you have a node, spend some time figuring out which of
            the leafs exactly your result belongs to.)
        :raises ValueError:
            Raised when confidence is not between 0 and 100.
        """
        origin = origin or ''
        if not isinstance(origin, str):
            origin = origin.__class__.__name__
        if severity not in RESULT_SEVERITY.reverse:
            raise ValueError('severity is not a valid RESULT_SEVERITY')

        self.origin = origin
        self.message = message
        self.debug_msg = debug_msg
        self.additional_info = additional_info
        # Sorting is important for tuple comparison
        self.affected_code = tuple(sorted(affected_code))
        self.severity = severity
        if confidence < 0 or confidence > 100:
            raise ValueError('Value of confidence should be between 0 and 100.')
        self.confidence = confidence
        self.diffs = diffs
        self.id = uuid.uuid4().int
        self.aspect = aspect

    @classmethod
    @enforce_signature
    def from_values(cls,
                    origin,
                    message: str,
                    file: str,
                    line: (int, None)=None,
                    column: (int, None)=None,
                    end_line: (int, None)=None,
                    end_column: (int, None)=None,
                    severity: int=RESULT_SEVERITY.NORMAL,
                    additional_info: str='',
                    debug_msg='',
                    diffs: (dict, None)=None,
                    confidence: int=100,
                    aspect: (aspectbase, None)=None):
        """
        Creates a result with only one SourceRange with the given start and end
        locations.

        :param origin:
            Class name or creator object of this object.
        :param message:
            Message to show with this result.
        :param file:
            The related file.
        :param line:
            The first related line in the file. (First line is 1)
        :param column:
            The column indicating the first character. (First character is 1)
        :param end_line:
            The last related line in the file.
        :param end_column:
            The column indicating the last character.
        :param severity:
            Severity of this result.
        :param additional_info:
            A long description holding additional information about the issue
            and/or how to fix it. You can use this like a manual entry for a
            category of issues.
        :param debug_msg:
            A message which may help the user find out why this result was
            yielded.
        :param diffs:
            A dictionary with filename as key and ``Diff`` object
            associated with it as value.
        :param confidence:
            A number between 0 and 100 describing the likelihood of this result
            being a real issue.
        :param aspect:
            An Aspect object which this result is associated to. Note that this
            should be a leaf of the aspect tree! (If you have a node, spend
            some time figuring out which of the leafs exactly your result
            belongs to.)
        """
        range = SourceRange.from_values(file,
                                        line,
                                        column,
                                        end_line,
                                        end_column)

        return cls(origin=origin,
                   message=message,
                   affected_code=(range,),
                   severity=severity,
                   additional_info=additional_info,
                   debug_msg=debug_msg,
                   diffs=diffs,
                   confidence=confidence,
                   aspect=aspect)

    def to_string_dict(self):
        """
        Makes a dictionary which has all keys and values as strings and
        contains all the data that the base Result has.

        FIXME: diffs are not serialized ATM.
        FIXME: Only the first SourceRange of affected_code is serialized. If
        there are more, this data is currently missing.

        :return: Dictionary with keys and values as string.
        """
        retval = {}

        members = ['id',
                   'additional_info',
                   'debug_msg',
                   'message',
                   'origin',
                   'confidence']

        for member in members:
            value = getattr(self, member)
            retval[member] = '' if value is None else str(value)

        retval['severity'] = str(RESULT_SEVERITY.reverse.get(
            self.severity, ''))
        if len(self.affected_code) > 0:
            retval['file'] = self.affected_code[0].file
            line = self.affected_code[0].start.line
            retval['line_nr'] = '' if line is None else str(line)
        else:
            retval['file'], retval['line_nr'] = '', ''

        return retval

    @enforce_signature
    def apply(self, file_dict: dict):
        """
        Applies all contained diffs to the given file_dict. This operation will
        be done in-place.

        :param file_dict: A dictionary containing all files with filename as
                          key and all lines a value. Will be modified.
        """
        for filename, diff in self.diffs.items():
            file_dict[filename] = diff.modified

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

    def overlaps(self, ranges):
        """
        Determines if the result overlaps with source ranges provided.

        :param ranges: A list SourceRange objects to check for overlap.
        :return:       True if the ranges overlap with the result.
        """
        if isinstance(ranges, SourceRange):
            ranges = [ranges]

        for range in ranges:
            for self_range in self.affected_code:
                if range.overlaps(self_range):
                    return True

        return False

    def location_repr(self):
        """
        Retrieves a string, that briefly represents
        the affected code of the result.

        :return: A string containing all of the affected files
                 separated by a comma.
        """

        if not self.affected_code:
            return 'the whole project'

        # Set important to exclude duplicate file names
        range_paths = set(sourcerange.file
                          for sourcerange in self.affected_code)

        return ', '.join(repr(relpath(range_path))
                         for range_path in sorted(range_paths))

    def __json__(self, use_relpath=False):
        _dict = get_public_members(self)
        if use_relpath and _dict['diffs']:
            _dict['diffs'] = {relpath(file): diff
                              for file, diff in _dict['diffs'].items()}
        _dict['aspect'] = type(self.aspect).__qualname__
        return _dict
