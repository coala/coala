from .base import aspectbase
from .meta import aspectclass
from .taste import Taste

__all__ = ['Root', 'Taste', 'aspectclass']


class Root(aspectbase, metaclass=aspectclass):
    """
    The root aspectclass.

    Define sub-aspectclasses with class-bound ``.subaspect`` decorator.
    Definition string is taken from doc-string of decorated class.
    Remaining docs are taken from a nested ``docs`` class.
    Tastes are defined as class attributes that are instances of
    :class:`coalib.bearlib.aspectclasses.Taste`.

    >>> @Root.subaspect
    ... class Formatting:
    ...     \"""
    ...     A parent aspect for code formatting aspects...
    ...     \"""

    >>> @Formatting.subaspect
    ... class LineLength:
    ...     \"""
    ...     This aspect controls the length of a line...
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

    >>> Root.Formatting.LineLength
    <aspectclass 'Root.Formatting.LineLength'>
    """
    parent = None

    _tastes = {}
