from .meta import aspectclass
from .taste import Taste

__all__ = ['Root', 'Taste']


class Root(metaclass=aspectclass):
    """The root aspectclass.

    Define sub-aspectclasses with class-bound ``.subaspect`` decorator.
    Definition string is taken from doc-string of decorated class.
    Remaining docs are taken from a nested ``docs`` class.
    Tastes are defined as class attributes that are instances of
    :class:`coalib.bearlib.aspectclasses.Taste`.
    The actual :class:`coalib.bearlib.aspects.Aspect` instances
    are stored as ``.aspect`` attributes of the sub-aspectclasses.

    >>> @Root.subaspect
    ... class Formatting:
    ...     pass

    >>> @Formatting.subaspect
    ... class LineLength:
    ...     \"""This aspect controls the length of a line...
    ...     \"""
    ...     class docs:
    ...        example = "..."
    ...        example_language = "..."
    ...        importance_reason = "..."
    ...        fix_suggestions = "..."
    ...
    ...     max_line_length = Taste[int](
    ...         "Maximum length allowed for a line.",
    ...         (80, 90, 120), default=80)

    >>> repr(Root.Formatting.LineLength)
    <coalib.bearlib.aspectclasses.aspectclass 'Root.Sample'>

    >>> type(Root.Formatting.LineLength.aspect)
    coalib.bearlib.aspects.Aspect
    """
    parent = None

    _tastes = {}
