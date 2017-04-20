from coalib.results.TextPosition import TextPosition
from coala_utils.decorators import enforce_signature


class AbsolutePosition(TextPosition):

    @enforce_signature
    def __init__(self,
                 text: (tuple, list, None)=None,
                 position: (int, None)=None):
        """
        Creates an AbsolutePosition object that represents the index of a
        character in a string.

        :param text:     The text containing the character.
        :param position: Position identifying the index of character
                         in text.
        """
        line = column = None
        if position is not None and text is not None:
            line, column = calc_line_col(text, position)
        self._text = text
        self._position = position
        super().__init__(line, column)

    @property
    def position(self):
        return self._position

    def __le__(self, other):
        """
        Test whether ``self`` is behind or equals the other
        ``AbsolutePosition``.

        :param other: ``AbsolutePosition`` to compare with.
        :return:      Whether this ``AbsolutePosition`` is behind the other
                      one or the same.
        """
        if not isinstance(other, self.__class__):
            return False

        if self._text != other._text:
            return False

        return self.position <= other.position

    def __ge__(self, other):
        """
        Test whether ``self`` is ahead of or equals the
        other ``AbsolutePosition``.

        :param other: ``AbsolutePosition`` to compare with.
        :return:      Whether this ``AbsolutePosition`` is ahead of the other
                      one or the same.
        """
        if not isinstance(other, self.__class__):
            return False

        if self._text != other._text:
            return False

        return self.position >= other.position

    def __lt__(self, other):
        """
        Test whether ``self`` is behind the other
        ``AbsolutePosition``.

        :param other: ``AbsolutePosition`` to compare with.
        :return:      Whether this ``AbsolutePosition`` is behind the other
                      one.
        """
        if not isinstance(other, self.__class__):
            return False

        if self._text != other._text:
            return False

        return self.position < other.position

    def __gt__(self, other):
        """
        Test whether ``self`` is ahead of the other
        ``AbsolutePosition``.

        :param other: ``AbsolutePosition`` to compare with.
        :return:      Whether this ``AbsolutePosition`` is ahead of the other
                      one.
        """
        if not isinstance(other, self.__class__):
            return False

        if self._text != other._text:
            return False

        return self.position > other.position

    def __eq__(self, other):
        """
        Test whether ``self`` equals the other ``AbsolutePosition``.

        :param other: ``AbsolutePosition`` to compare with.
        :return:      Whether this ``AbsolutePosition`` equals the
                      other.
        """
        if not isinstance(other, self.__class__):
            return False

        if self._text != other._text:
            return False

        return self.position == other.position


def calc_line_col(text, position):
    r"""
    Creates a tuple containing (line, column) by calculating line number
    and column in the text, from position.

    The position represents the index of a character. In the following
    example 'a' is at position '0' and it's corresponding line and column are:

    >>> calc_line_col(('a\n',), 0)
    (1, 1)

    All special characters(including the newline character) belong in the same
    line, and have their own position. A line is an item in the tuple:

    >>> calc_line_col(('a\n', 'b\n'), 1)
    (1, 2)
    >>> calc_line_col(('a\n', 'b\n'), 2)
    (2, 1)

    :param text:          A tuple/list of lines in which position is to
                          be calculated.
    :param position:      Position (starting from 0) of character to be found
                          in the (line, column) form.
    :return:              A tuple of the form (line, column), where both line
                          and column start from 1.
    """
    for linenum, line in enumerate(text, start=1):
        linelen = len(line)
        if position < linelen:
            return linenum, position + 1
        position -= linelen

    raise ValueError('Position not found in text')
