from coala_utils.decorators import enforce_signature


class TasteMeta(type):
    """Metaclass for :class:`coalib.bearlib.aspectclasses.Taste`

    Allows defining taste cast type via :meth:`.__getitem__`, like::

       Taste[int](...)
    """
    def __getitem__(cls, _cast_type):
        class Taste(cls):
            cast_type = _cast_type

        Taste.__name__ = Taste.__qualname__ = "%s[%s]" % (
            cls.__name__, _cast_type.__name__)
        return Taste


class Taste(metaclass=TasteMeta):
    """Defines tastes in aspectclass definitions.

    See :class:`coalib.bearlib.aspectclasses.Root` for usage.
    """
    cast_type = str

    @enforce_signature
    def __init__(self, description: str="", suggested_values: tuple=(),
                 default=None):
        """No need to specify name an cast type:

        The taste name is defined by the taste's attribute name in an
        aspectclass definition.

        The value cast type is defined via indexing on class level.
        """
        self.description = description
        self.suggested_values = suggested_values
        self.default = default

    def __get__(self, obj, owner=None):
        """Descriptor interface for accessing tastes in aspectclasses.

        Returns `self` when accessed from an aspectclass and its specific
        taste value from an aspectclass instance.
        """
        if obj is not None:
            # ==> access from instance
            # ==> return specific aspect taste value
            return obj.__dict__[self.name]

        if owner is not None:
            # ==> access from class
            return self
