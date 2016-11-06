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

    We can now create subaspects like this:

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

    The representation will show the full "path" to the leaf of the tree:

    >>> Root.Formatting.LineLength
    <aspectclass 'Root.Formatting.LineLength'>

    We can see, which settings are availables:

    >>> Formatting.tastes
    {}
    >>> LineLength.tastes  # +ELLIPSIS
    {'max_line_length': <....Taste[int] object at ...>}

    And instanciate the aspect with the values, they will be automatically
    converted:

    >>> Formatting()  # +ELLIPSIS
    <coalib.bearlib.aspects.Root.Formatting object at 0x...>
    >>> LineLength(max_line_length="100").tastes
    {'max_line_length': 100}

    If no settings are given, the defaults will be taken>
    >>> LineLength().tastes
    {'max_line_length': 80}
    """
    parent = None

    _tastes = {}
