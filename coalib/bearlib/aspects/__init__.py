"""
This package contains all aspects that bears can detect or fix and their
documentation.
"""

from inspect import cleandoc

from coala_utils.decorators import (
    classproperty, enforce_signature, generate_consistency_check)


@generate_consistency_check('definition', 'cause', 'example',
                            'example_language', 'importance_reason',
                            'fix_suggestions')
class AspectDocumentation:
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


@generate_consistency_check(
    'name', 'description', 'cast_type', 'suggested_values')
class AspectSetting:
    """
    This class contains the specification about a setting that should be given
    for an aspect.
    """

    class NoDefault:
        pass

    @enforce_signature
    def __init__(self,
                 name: str='',
                 description: str='',
                 cast_type=str,
                 suggested_values: tuple=(),
                 default=NoDefault):
        """
        Instantiates an ``AspectSetting`` object.

        :param name:
            Name of the setting.
        :param description:
            A description of what the setting is about and what it does.
        :param cast_type:
            The type to cast the user value into. For example, ``int`` will
            convert and setting value as an integer.
        :param suggested_values:
            A tuple of suggested values that help the user understand what
            kind of values this setting takes.
        :param default:
            Default value for the setting. (Optional)
        """
        self.name = name
        self.description = cleandoc(description)
        self.cast_type = cast_type
        self.suggested_values = suggested_values
        self.default = default


class Aspect:
    '''
    This is the ``Aspect`` base class. Each aspect may have sub-aspects,
    which are ``Aspect`` objects themselves. An aspect also contains
    documentation, instantiated as an ``AspectDocumentation`` object.

    There is a root ``Aspect`` object in which every other aspect lives.

    >>> Root = Aspect()

    This is a placeholder aspect through which every other aspect can be
    accessed.

    To create new aspect, simply call the ``new_subaspect`` method with
    the subaspect's name as a param, along with its documentation (mandatory
    for each aspect):

    >>> Root.new_subaspect(
    ...     "Redundancy",
    ...     doc=AspectDocumentation(
    ...         """
    ...         This aspect describes redundancy in your source code. Those are
    ...         usually places where you can strip away source code in order to
    ...         make your codebase better maintainable but keeping your full
    ...         functionality.
    ...         """, '...', '...', '...'
    ...     )
    ... )

    This aspect is now accesible at ``Root.Redundancy``. Simply call
    ``new_subaspect`` to keep creating new sub-aspects:

    >>> Root.Redundancy.new_subaspect(
    ...     "Clone",
    ...     doc=AspectDocumentation(
    ...         "This aspect describes clones in your source code...",
    ...         '...', '...' ,'...'
    ...     )
    ... )

    And this aspect will be available at ``Root.Redundancy.Clone``.

    Trying to access an undefined aspect will raise a ``NameError``:

    >>> Root.UnknownAspect is None
    Traceback (most recent call last):
      ...
    NameError

    And of course, you can create settings for your aspects:

    >>> Root.Redundancy.Clone.settings = [
    ...     AspectSetting("min_clone_token",
    ...                   "The number of tokens that have to be "
    ...                   "equal for it to be detected as a code clone",
    ...                   int, suggested_values=(20, 40, 60), default=20)
    ... ]

    ``settings`` can be defined for any aspect by creating a list of
    ``AspectSetting`` objects with 5 params:

        * the setting name
        * a documentation string
        * a cast type (in this case ``int`` will be applied to the given
          setting)
        * a tuple of example values that the setting might take
        * (optional) the default value for the setting.

    Please refer to the docs for the ``AspectSetting`` class to learn more.

    All bears implementing a given aspect should implement all the settings
    given and documented by it. Additional bear specific settings might be
    added to allow further configuration.

    You can also give the settings at object instantiation using the
    ``settings`` param. Each setting can also contain a param called
    ``suggested_values`` - these are helpful for the user to understand
    what the setting does and what values it may take:

    >>> Root.new_subaspect("Formatting", doc=AspectDocumentation(
    ...     "...", "...", "...", "..."))
    >>> Root.Formatting.new_subaspect(
    ...     "LineLength",
    ...     doc=AspectDocumentation(
    ...         "This aspect controls the length of a line...",
    ...         '...', '...', '...'
    ...     ),
    ...     settings=[
    ...         AspectSetting(
    ...             "min_line_length",
    ...             "Maximum length allowed for a line.",
    ...             int,
    ...             suggested_values=(80, 90, 120),
    ...             default=80
    ...         )
    ...     ]
    ... )
    >>> Root.Formatting.LineLength.settings[0].suggested_values
    (80, 90, 120)

    Settings are inherited by sub-aspects:

    >>> Root.Redundancy.Clone.new_subaspect(
    ...     "Logic",
    ...     doc=AspectDocumentation(
    ...         "This aspect describes redundant logic in your code",
    ...         '...', '...', '...'
    ...     )
    ... )
    >>> [(setting.name, setting.default)
    ...  for setting in Root.Redundancy.Clone.Logic.settings]
    [('min_clone_token', 20)]

    This permeates for every subsequent sub-aspect too. Also note that
    a changes to a setting of an aspect will be reflected in every sub-aspect
    too.

    >>> Root.Redundancy.Clone.settings = [
    ...     AspectSetting("min_clone_token",
    ...                   "The number of tokens that have to be "
    ...                   "equal for it to be detected as a code clone",
    ...                   int, default=30)
    ... ]

    >>> Root.Redundancy.Clone.settings[0].default
    30
    >>> Root.Redundancy.Clone.Logic.settings[0].default
    30

    If you don't want this, you can override the settings the particular
    sub-aspect:

    >>> Root.Redundancy.Clone.Logic.settings = [
    ...     AspectSetting("min_clone_token",
    ...                   "The number of tokens that have to be "
    ...                   "equal for it to be detected as a code clone",
    ...                   int, default=40)
    ... ]

    >>> Root.Redundancy.Clone.settings[0].default
    30
    >>> Root.Redundancy.Clone.Logic.settings[0].default
    40

    The user can use the qualifying name according to PEP 3155 for selecting
    and unselecting aspects (see <https://www.python.org/dev/peps/pep-3155/>):

    >>> Root.Redundancy.Clone.__qualname__
    'Redundancy.Clone'

    The ``Root`` part of the aspect is removed for brevity.
    '''

    @generate_consistency_check('name', 'doc')
    def __init__(self,
                 name="Root",
                 doc=None,
                 settings=[],
                 parent=None):
        """
        Instantiates the ``Aspect`` object.

        :param name:
            Name of the aspect.
        :param parent:
            A reference to the parent object for this aspect. For first-level
            aspects, this is the root aspect.
        """
        self.__name__ = name
        self.docs = doc
        self.subaspects = {}
        self.parent = parent
        self._settings = settings
        if self.parent and self.parent.__name__ != "Root":
            self.__qualname__ = self.parent.__qualname__ + "." + self.__name__
        else:
            self.__qualname__ = self.__name__

    def new_subaspect(self, name, doc, settings=[]):
        """
        Creates a sub-aspect.

        :param name:
            Name of the sub-aspect.
        """
        self.subaspects[name] = Aspect(
            name,
            doc=doc,
            settings=settings,
            parent=self)

    def __getattr__(self, subaspect):
        """
        Returns the sub-aspect.

        :param subaspect:
            Name of the sub-aspect. This should have been instantiated
            previously using the ``new_subaspect`` method.
        :return:
            An ``Aspect`` object corresponding to the sub-aspect. If the
            sub-aspect is not found, ``None`` is returned.
        """
        if subaspect in self.subaspects:
            return self.subaspects[subaspect]
        raise NameError

    @property
    def settings(self):
        current = self
        taken_settings = set()
        result = []

        # Recursively go up and collect settings (the most local setting
        # overrides previous values)
        while current is not None:
            for setting in current._settings:
                if setting.name not in taken_settings:
                    taken_settings.add(setting.name)
                    result.append(setting)
            current = current.parent

        return result

    @settings.setter
    def settings(self, value):
        self._settings = value
