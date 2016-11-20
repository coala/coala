from coala_utils.decorators import enforce_signature

from coalib.bearlib.languages import Language


class TasteMeta(type):
    """
    Metaclass for :class:`coalib.bearlib.aspectclasses.Taste`

    Allows defining taste cast type via :meth:`.__getitem__`, like::

       Taste[int](...)
    """
    class Languages(tuple):
        """
        A ``tuple``-based container for
        :class:`coalib.bearlib.languages.Language` instances.

        It supports language identifiers in any format accepted by
        ``Language[...]`` and provides :meth:`.__contains__` for checking
        if a given language identifier is included:

        >>> 'Python 2.7, 3.5' in Taste.Languages([Language.Python()])
        True
        >>> 'Py 3.3' in Taste.Languages(['Python 2'])
        False
        >>> 'csharp' in Taste.Languages(['C#', Language.Python == 3])
        True
        """

        def __new__(cls, items):
            return tuple.__new__(cls, (Language[i] for i in items))

        def __contains__(self, item):
            return any(item in lang for lang in self)

    def __getitem__(cls, _cast_type):
        class Taste(cls):
            cast_type = _cast_type

        Taste.__name__ = Taste.__qualname__ = '%s[%s]' % (
            cls.__name__, _cast_type.__name__)
        return Taste


class Taste(metaclass=TasteMeta):
    """
    Defines tastes in aspectclass definitions.

    See :class:`coalib.bearlib.aspectclasses.Root` for usage.
    """
    cast_type = str

    @enforce_signature
    def __init__(self, description: str='', suggested_values: tuple=(),
                 default=None, languages: tuple=()):
        """
        No need to specify name and cast type:

        The taste name is defined by the taste's attribute name in an
        aspectclass definition.

        The value cast type is defined via indexing on class level.
        """
        self.description = description
        self.suggested_values = suggested_values
        self.default = default
        self.languages = type(self).Languages(languages)
