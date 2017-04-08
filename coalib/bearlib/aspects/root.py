from .base import aspectbase
from .meta import aspectclass


class Root(aspectbase, metaclass=aspectclass):
    """
    The root aspectclass.

    Define sub-aspectclasses with class-bound ``.subaspect`` decorator.
    Definition string is taken from doc-string of decorated class.
    Remaining docs are taken from a nested ``docs`` class.
    Tastes are defined as class attributes that are instances of
    :class:`coalib.bearlib.aspects.Taste`.

    >>> from coalib.bearlib.aspects import Taste

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
    >>> LineLength.tastes
    {'max_line_length': <....Taste[int] object at ...>}

    And instantiate the aspect with the values, they will be automatically
    converted:

    >>> Formatting('Python')
    <....Root.Formatting object at 0x...>
    >>> LineLength('Python', max_line_length="100").tastes
    {'max_line_length': 100}

    If no settings are given, the defaults will be taken:

    >>> LineLength('Python').tastes
    {'max_line_length': 80}

    Tastes can also be made available for only specific languages:

    >>> from coalib.bearlib.languages import Language
    >>> @Language
    ... class GreaterTrumpScript:
    ...     pass

    >>> @Formatting.subaspect
    ... class Greatness:
    ...     \"""
    ...     This aspect controls the greatness of a file...
    ...     \"""
    ...
    ...     min_greatness = Taste[int](
    ...         "Minimum greatness factor needed for a TrumpScript file. "
    ...         "This is fact.",
    ...         (1000000, 1000000000, 1000000000000), default=1000000,
    ...         languages=('GreaterTrumpScript' ,))

    >>> Greatness.tastes
    {'min_greatness': <....Taste[int] object at ...>}
    >>> Greatness('GreaterTrumpScript').tastes
    {'min_greatness': 1000000}
    >>> Greatness('GreaterTrumpScript', min_greatness=1000000000000).tastes
    {'min_greatness': 1000000000000}

    >>> Greatness('Python').tastes
    {}

    >>> Greatness('Python', min_greatness=1000000000)
    ... # doctest: +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
      ...
    coalib.bearlib.aspects.taste.TasteError:
    Root.Formatting.Greatness.min_greatness is not available ...

    >>> Greatness('Python').min_greatness
    ... # doctest: +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
      ...
    coalib.bearlib.aspects.taste.TasteError:
    Root.Formatting.Greatness.min_greatness is not available ...
    """
    parent = None

    _tastes = {}
