from coala_utils.decorators import enforce_signature

from coalib.bearlib.languages import Languages


class TasteError(AttributeError):
    """
    A taste is not allowed to be accessed.
    """


class TasteMeta(type):
    """
    Metaclass for :class:`coalib.bearlib.aspects.Taste`

    Allows defining taste cast type via :meth:`.__getitem__`, like:

    >>> Taste[int]().cast_type
    <class 'int'>
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

    Tastes can be made only available for certain languages by
    providing a ``tuple`` of language identifiers on instantiation:

    >>> Taste[bool](
    ...     'Ignore ``using`` directives in C#.',
    ...     (True, False), default=False,
    ...     languages=('CSharp', )
    ... ).languages
    (C#,)

    If no `languages` are given, they will be available for any language.
    See :class:`coalib.bearlib.aspects.Root` for further usage.
    """
    cast_type = str

    @enforce_signature
    def __init__(self, description: str='', suggested_values: tuple=(),
                 default=None, languages: tuple=()):
        """
        Creates a new taste that can be optionally only available for the
        given `languages`, which must be language identifiers supported by
        :class:`coalib.bearlib.languages.Language`.

        No need to specify the cast type:

        The taste name is defined by the taste's attribute name in an
        aspectclass definition.

        The value cast type is defined via indexing on class level.

        :param description:         Description of the taste.
        :param suggested_values:    A tuple containing the list of possible
                                    values for the taste.
        :param default:             Default value of the taste.
        :param languages:           A tuple containing list of languages, for
                                    which the taste is defined.
        """
        self.description = description
        self.suggested_values = suggested_values
        self.default = default
        self.languages = Languages(languages)

    def __get__(self, obj, owner=None):
        """
        Checks availability of taste for aspectclass instance `obj`'s
        ``.language`` before returning the specific taste value.
        """
        if obj is not None:
            # ==> access from aspectclass instance
            if self.languages and obj.language not in self.languages:
                raise TasteError('%s.%s is not available for %s.' % (
                    type(obj).__qualname__, self.name, obj.language))
            return obj.__dict__[self.name]
        # ==> access from aspectclass
        return self

    def __set__(self, obj, value):
        """
        Ensures that `value` is only set once in `obj`'s ``.__dict__``.
        """
        if self.name in obj.__dict__:
            raise AttributeError(
                "A 'taste' value for this aspectclass instance "
                'exists already.')
        obj.__dict__[self.name] = self.cast_type(value)
