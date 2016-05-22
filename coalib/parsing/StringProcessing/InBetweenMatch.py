from coala_decorators.decorators import generate_ordering, generate_repr
from coalib.parsing.StringProcessing import Match


@generate_repr("begin", "inside", "end")
@generate_ordering("begin", "inside", "end")
class InBetweenMatch:
    """
    Holds information about a match enclosed by two matches.
    """

    def __init__(self, begin, inside, end):
        """
        Instantiates a new InBetweenMatch.

        :param begin:  The ``Match`` of the start pattern.
        :param inside: The ``Match`` between start and end.
        :param end:    The ``Match`` of the end pattern.
        """
        if begin > inside or inside > end:
            raise ValueError("The inside match must be enclosed by the begin "
                             "and end match.")

        self._begin = begin
        self._inside = inside
        self._end = end

    @classmethod
    def from_values(cls, begin, begin_pos, inside, inside_pos, end, end_pos):
        """
        Instantiates a new InBetweenMatch from Match values.

        This function allows to bypass the usage of Match object instantation:

        >>> a = InBetweenMatch(Match("A", 0), Match("B", 1), Match("C", 2))
        >>> b = InBetweenMatch.from_values("A", 0, "B", 1, "C", 2)
        >>> assert a == b

        :param begin:      The matched string from start pattern.
        :param begin_pos:  The position of the matched begin string.
        :param inside:     The matched string from inside/in-between pattern.
        :param inside_pos: The position of the matched inside/in-between
                           string.
        :param end:        The matched string from end pattern.
        :param end_pos:    The position of the matched end string.
        :returns:          An InBetweenMatch from the given values.
        """
        return cls(Match(begin, begin_pos),
                   Match(inside, inside_pos),
                   Match(end, end_pos))

    @property
    def begin(self):
        return self._begin

    @property
    def inside(self):
        return self._inside

    @property
    def end(self):
        return self._end
