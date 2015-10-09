from functools import total_ordering

from coalib.misc.Decorators import generate_repr


@generate_repr("file", "line")
@total_ordering
class SourcePosition:
    def __init__(self, file=None, line=None):
        """
        Creates a new result position object that represents the position of a
        result in the source code.

        :param file:            The filename or None.
        :param line:            The line in file or None.
        :raises AssertionError: If a line number without a file is provided.
        """
        self.file = file
        self.line = line

    @property
    def line(self):
        return self._line

    @line.setter
    def line(self, other):
        assert self.file is not None or other is None
        self._line = other

    def __str__(self):
        return "file: {}, line: {}".format(
            str(repr(self.file)),
            str(self.line))

    def __eq__(self, other):
        if not isinstance(other, SourcePosition):
            return False

        return (self.file == other.file and
                self.line == other.line)

    def __lt__(self, other):
        return lt(self, other)


@generate_repr("start", "end")
@total_ordering
class SourceRange:
    def __init__(self, start, end):
        if not isinstance(start, SourcePosition):
            raise TypeError("The start of this SourceRange is not a "
                            "SourcePosition")

        if not isinstance(end, SourcePosition):
            raise TypeError("The end of this SourceRange is not a "
                            "SourcePosition")

        if not start.file == end.file:
            raise ValueError("Start and end of this SourceRange are not"
                             "located in the same file")

        if not end >= start:
            raise ValueError("The Start of this SourceRange lies after it's "
                             "end")

        self.start = start
        self.end = end

    def __eq__(self, other):
        if not isinstance(other, SourceRange):
            return False

        return self.start == other.start and self.end == other.end

    def __lt__(self, other):
        return lt(self, other)


def lt(source_object, other):
    # source_object can only be SourcePosition or SourceRange
    if not (isinstance(other, SourcePosition) or
            isinstance(other, SourceRange)):
        raise TypeError("SourceArea objects can only be compared with "
                        "each other")

    if isinstance(source_object, SourcePosition):
        if isinstance(other, SourcePosition):
            return _lt_positions(source_object, other)

        else:
            return _lt_position_vs_range(source_object, other)

    else:
        if isinstance(other, SourcePosition):
            # ranges and positions cannot be equal, therefore this is valid:
            return not _lt_position_vs_range(other, source_object)

        else:
            return _lt_ranges(source_object, other)


def _lt_positions(position, other_position):
    if (position.file is None) != (other_position.file is None):
        return position.file is None

    if position.file != other_position.file:
        return position.file < other_position.file

    if (position.line is None) != (other_position.line is None):
        return position.line is None

    if position.line != other_position.line:
        return position.line < other_position.line

    return False


def _lt_position_vs_range(position, other_range):
    if position == other_range.start:
        return True  # position < range

    return position < other_range.start


def _lt_ranges(range, other_range):
    if range.start != other_range.start:
        return range.start < other_range.start

    return range.end < other_range.end
