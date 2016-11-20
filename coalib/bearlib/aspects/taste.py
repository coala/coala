from coala_utils.decorators import enforce_signature


class TasteMeta(type):
    """
    Metaclass for :class:`coalib.bearlib.aspectclasses.Taste`

    Allows defining taste cast type via :meth:`.__getitem__`, like::

       Taste[int](...)
    """
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
                 default=None):
        """
        No need to specify name an cast type:

        The taste name is defined by the taste's attribute name in an
        aspectclass definition.

        The value cast type is defined via indexing on class level.
        """
        self.description = description
        self.suggested_values = suggested_values
        self.default = default
