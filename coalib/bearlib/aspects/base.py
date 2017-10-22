import functools
import re

from coalib.bearlib.languages import Language

import coalib.bearlib.aspects
from .taste import TasteError


def get_subaspect(parent, subaspect):
    """
    Get a subaspect from an aspectclass or aspectclass instance.

    >>> import coalib.bearlib.aspects as coala_aspects
    >>> metadata = coala_aspects['Metadata']
    >>> commit_msg = coala_aspects['CommitMessage']
    >>> shortlog = coala_aspects['Shortlog']

    We can get direct children.

    >>> get_subaspect(metadata, commit_msg)
    <aspectclass 'Root.Metadata.CommitMessage'>

    Or even a grandchildren.

    >>> get_subaspect(metadata, shortlog)
    <aspectclass 'Root.Metadata.CommitMessage.Shortlog'>

    Or with string of aspect name

    >>> get_subaspect(metadata, 'shortlog')
    <aspectclass 'Root.Metadata.CommitMessage.Shortlog'>

    We can also get child instance of an aspect instance.

    >>> get_subaspect(metadata('Python'), commit_msg)
    <...CommitMessage object at 0x...>

    But, passing subaspect instance as argument is prohibited, because
    it doesn't really make sense.

    >>> get_subaspect(metadata('Python'), commit_msg('Java'))
    Traceback (most recent call last):
    ...
    AttributeError: Cannot search an aspect instance using another ...

    :param parent:    The parent aspect that should be searched.
    :param subaspect: An subaspect that we want to find in an
                      aspectclass.
    :return:          An aspectclass. Return None if not found.
    """
    # Avoid circular import
    from .meta import isaspect, issubaspect
    if not isaspect(subaspect):
        subaspect = coalib.bearlib.aspects[subaspect]
    if not issubaspect(subaspect, parent):
        return None
    if isinstance(subaspect, aspectbase):
        raise AttributeError('Cannot search an aspect instance using '
                             'another aspect instance as argument.')

    parent_qualname = (type(parent).__qualname__ if isinstance(
                       parent, aspectbase) else parent.__qualname__)
    if parent_qualname == subaspect.__qualname__:
        return parent

    # Trim common parent name
    aspect_path = re.sub(r'^%s\.' % parent_qualname, '',
                         subaspect.__qualname__)
    aspect_path = aspect_path.split('.')
    child = parent
    # Traverse through children until we got our subaspect
    for path in aspect_path:
        child = child.subaspects[path]
    return child


def _get_leaf_aspects(aspect):
    """
    Explode an aspect into list of its leaf aspects.

    :param aspect:    An aspect class or instance.
    :return:          List of leaf aspects.
    """
    # Avoid circular import
    from .collections import AspectList
    leaf_aspects = AspectList()

    def search_leaf(aspects):
        for aspect in aspects:
            if not aspect.subaspects:
                nonlocal leaf_aspects
                leaf_aspects.append(aspect)
            else:
                search_leaf(aspect.subaspects.values())

    search_leaf([aspect])
    return leaf_aspects


class SubaspectGetter:
    """
    Special "getter" class to implement ``get()`` method in aspectbase that
    could be accessed from the aspectclass or aspectclass instance.
    """

    def __get__(self, obj, owner):
        parent = obj if obj is not None else owner
        return functools.partial(get_subaspect, parent)


class LeafAspectGetter:
    """
    Descriptor class for ``get_leaf_aspects()`` method in aspectbase.

    This class is required to make the ``get_leaf_aspects()`` accessible from
    both aspectclass and aspectclass instance.
    """

    def __get__(self, obj, owner):
        parent = obj if obj is not None else owner
        return functools.partial(_get_leaf_aspects, parent)


class aspectbase:
    """
    Base class for aspectclasses with common features for their instances.

    Derived classes must use
    :class:`coalib.bearlib.aspects.meta.aspectclass` as metaclass.
    This is automatically handled by
    :meth:`coalib.bearlib.aspects.meta.aspectclass.subaspect` decorator.
    """

    get = SubaspectGetter()
    get_leaf_aspects = LeafAspectGetter()

    def __init__(self, language, **taste_values):
        """
        Instantiate an aspectclass with specific `taste_values`,
        including parent tastes.

        Given tastes must be available for the given `language`,
        which must be a language identifier supported by
        :class:`coalib.bearlib.languages.Language`.

        All taste values will be casted to the related taste cast types.

        Non-given available tastes will get their default values.
        """
        # bypass self.__setattr__
        self.__dict__['language'] = Language[language]
        for name, taste in type(self).tastes.items():
            if taste.languages and language not in taste.languages:
                if name in taste_values:
                    raise TasteError('%s.%s is not available for %s.' % (
                        type(self).__qualname__, name, language))
            else:
                setattr(self, name, taste_values.get(name, taste.default))
        # Recursively instance its subaspects too
        instanced_child = {}
        for name, child in self.subaspects.items():
            instanced_child[name] = child(language, **taste_values)
        self.__dict__['subaspects'] = instanced_child

    def __eq__(self, other):
        return type(self) is type(other) and self.tastes == other.tastes

    @property
    def tastes(self):
        """
        Get a dictionary of all taste names mapped to their specific values,
        including parent tastes.
        """
        return {name: self.__dict__[name] for name in type(self).tastes
                if name in self.__dict__}

    def __setattr__(self, name, value):
        """
        Don't allow attribute manipulations after instantiation of
        aspectclasses.
        """
        if name not in type(self).tastes:
            raise AttributeError(
                "can't set attributes of aspectclass instances")
        super().__setattr__(name, value)
