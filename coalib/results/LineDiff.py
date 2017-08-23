import collections

from coala_utils.decorators import generate_repr


class ConflictError(Exception):
    pass


@generate_repr('change', 'delete', 'add_after')
class LineDiff:
    """
    A LineDiff holds the difference between two strings.
    """

    def __init__(self, change=False, delete=False, add_after=False):
        """
        Creates a new LineDiff object. Note that a line cannot be
        changed _and_ deleted at the same time.

        :param change: False or a tuple (original, replacement)
        :param delete: True/False
        :param add_after: False or a list of lines to append after this ones
        """
        # change property setter will need this value for assertion
        self._delete = False

        self.change = change
        self.delete = delete
        self.add_after = add_after

    def __eq__(self, other):
        return (self.change == other.change and
                self.delete == other.delete and
                self.add_after == other.add_after)

    @property
    def change(self):
        return self._change

    @change.setter
    def change(self, value):
        if value is not False and not isinstance(value, tuple):
            raise TypeError('change must be False or a tuple with an original '
                            'and a replacement string.')
        if value is not False and self.delete is not False:
            raise ConflictError('A line cannot be changed and deleted '
                                'at the same time.')

        self._change = value

    @property
    def delete(self):
        return self._delete

    @delete.setter
    def delete(self, value):
        if not isinstance(value, bool):
            raise TypeError('delete can only be a boolean value.')
        if value is not False and self.change is not False:
            raise ConflictError('A line cannot be changed and deleted '
                                'at the same time.')

        self._delete = value

    @property
    def add_after(self):
        return self._add_after

    @add_after.setter
    def add_after(self, value):
        if value is not False and not isinstance(value, collections.Iterable):
            raise TypeError(
                'add_after must be False or a list of lines to append.')
        if isinstance(value, collections.Iterable):
            value = list(value)
        self._add_after = value if value != [] else False
