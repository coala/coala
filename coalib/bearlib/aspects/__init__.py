"""
This package contains all aspects that bears can detect or fix and their
documentation.
"""

from collections import namedtuple
from inspect import cleandoc

from coala_utils.decorators import classproperty, enforce_signature
from coalib.bearlib.naming_conventions import to_snakecase


class ConsistencyCheckMixin:
    """
    A mixin that can be inherited from and offers a ``check_consistency``
    method.
    """

    def check_consistency(self):
        """
        Checks the consistency of the self object. Consistency is given, if all
        members of the object evaluate to ``True``.

        :return: ``True`` or ``False``
        """
        return all(getattr(self, key)
                   for key in dir(self)
                   if not key.startswith('_'))


class AspectDocumentation(ConsistencyCheckMixin):
    """
    This class contains documentation about an aspect described by the Aspect
    class.

    The documentation is consistent if all members are given:

    >>> AspectDocumentation('defined', '', '', '').check_consistency()
    False
    >>> AspectDocumentation('definition', 'cause', 'example',
    ...                     'example_language', 'importance',
    ...                     'fix').check_consistency()
    True
    """

    @enforce_signature
    def __init__(self, definition: str='', cause: str='', example: str='',
                 example_language: str='', importance_reason: str='',
                 fix_suggestions: str=''):
        """
        Contains documentation for an aspect.

        :param definition:        What is this about?
        :param cause:             Information on how such a problem can happen.
        :param example:           An example in a well known language.
        :param example_language:  The language used for the example.
        :param importance_reason: A reason why this aspect is important.
        :param fix_suggestions:   Suggestions on how this can be fixed.
        """
        super().__init__()

        self.definition = cleandoc(definition)
        self.cause = cleandoc(cause)
        self.example = cleandoc(example)
        self.example_language = cleandoc(example_language)
        self.importance_reason = cleandoc(importance_reason)
        self.fix_suggestions = cleandoc(fix_suggestions)


class Aspect:
    '''
    This is the Aspect base class. You can use it to define aspects (and sub
    aspects recursively) including their documentation and meaningful
    settings.

    In order to create an aspect, just inherit the class from Aspect. To make
    a subaspect, define a nested class within any aspect and inherit from it.
    (coala will figure out which aspect belongs where via the inheritance and
    it looks nice to use an aspect when they're defined nested.)

    >>> class Redundancy(Aspect):
    ...     docs = AspectDocumentation(
    ...         """
    ...         This aspect describes redundancy in your source code. Those are
    ...         usually places where you can strip away source code in order to
    ...         make your codebase better maintainable but keeping your full
    ...         functionality.
    ...         """, '...', '...', '...'
    ...     )
    ...
    ...     class Clone(Aspect):
    ...         docs = AspectDocumentation(
    ...             """
    ...             Code clones are different pieces of code in your codebase that
    ...             are very similar.
    ...             """, '...', '...',
    ...             """
    ...             Usually code clones can be simplified to only one occurrence...
    ...             """
    ...         )
    ...         MIN_CLONE_TOKEN = ("The number of tokens that have to be "
    ...                            "equal for it to be detected as a code "
    ...                            "clone.", int, 20)

    As we see in the example above, we can define settings for any aspect class
    by providing a tuple of a documentation string, a conversion function (in
    this case ``int`` will be applied to the given setting) and an optional
    default value if the setting is not mandatory.

    >>> Redundancy.Clone.settings  # doctest: +ELLIPSIS
    {'min_clone_token': ('The number of tokens...', <class 'int'>, 20)}

    All bears implementing a given aspect should implement all the settings
    given and documented by it. Additional bear specific settings might be
    added to allow further configuration.

    The user can use the qualifying name according to PEP 3155 for selecting
    and unselecting aspects (see <https://www.python.org/dev/peps/pep-3155/>):

    >>> Redundancy.Clone.__qualname__
    'Redundancy.Clone'
    '''

    docs = AspectDocumentation('', '', '', '')

    def __init__(self):
        """
        Do not instanciate this class.

        >>> Aspect()
        Traceback (most recent call last):
         ...
        AssertionError: This class should not be instanciated.

        Really. Don't. Ever.
        """
        raise AssertionError("This class should not be instanciated.")

    @classproperty
    def settings(cls) -> {"setting_name": ("Description", int, 20)}:
        """
        Retrieves settings that should be present for any routine that checks
        this aspect.

        :return:
            A dictionary of setting names as key and a tuple of a description,
            a type conversion routine and optionally a default value.
        """
        return {key.lower(): getattr(cls, key)
                for key in dir(cls)
                if key.isupper() and not key.startswith('_')}
