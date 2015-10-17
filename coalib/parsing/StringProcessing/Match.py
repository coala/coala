from coalib.misc.Decorators import generate_ordering, generate_repr


@generate_repr("match", "range")
@generate_ordering("range", "match")
class Match:
    """
    Stores information about a single textual match.
    """

    def __init__(self, match, position):
        """
        Instantiates a new Match.

        :param match:    The actual matched string.
        :param position: The position where the match was found. Starts from
                         zero.
        """
        self._match = match
        self._position = position

    def __len__(self):
        return len(self.match)

    def __str__(self):
        return self.match

    @property
    def match(self):
        """
        Returns the text matched.

        :returns: The text matched.
        """
        return self._match

    @property
    def position(self):
        """
        Returns the position where the text was matched (zero-based).

        :returns: The position.
        """
        return self._position

    @property
    def end_position(self):
        """
        Marks the end position of the matched text (zero-based).

        :returns: The end-position.
        """
        return len(self) + self.position

    @property
    def range(self):
        """
        Returns the position range where the text was matched.

        :returns: A pair indicating the position range. The first element is
                  the start position, the second one the end position.
        """
        return (self.position, self.end_position)
