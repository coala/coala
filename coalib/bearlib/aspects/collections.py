import itertools

import coalib.bearlib.aspects
from coalib.bearlib.aspects.meta import isaspect, issubaspect
from coalib.bearlib.aspects.base import aspectbase


class AspectList(list):
    """
    List-derived container to hold aspects.
    """

    def __init__(self, seq=(), exclude=None, languages=None):
        """
        Initialize a new AspectList.

        >>> from .Metadata import CommitMessage
        >>> AspectList([CommitMessage.Shortlog, CommitMessage.Body])
        [<aspectclass '...Shortlog'>, <aspectclass '...Body'>]
        >>> AspectList(['Shortlog', 'CommitMessage.Body'])
        [<aspectclass '...Shortlog'>, <aspectclass '...Body'>]
        >>> AspectList([CommitMessage.Shortlog, 'CommitMessage.Body'])
        [<aspectclass '...Shortlog'>, <aspectclass '...Body'>]

        :param seq: A sequence containing either aspectclass, aspectclass
                    instance, or string of partial/full qualified aspect name.
        :param exclude: A sequence of either aspectclass or string of aspect
                        name that marked as excluded from the list.
        """
        super().__init__((item if isaspect(item) else
                          coalib.bearlib.aspects[item] for item in seq))

        self.languages = languages
        self.exclude = AspectList(exclude) if exclude is not None else []

    def __contains__(self, aspect):
        # Check if ``aspects`` language is supported.
        if self.languages is not None and isinstance(aspect, aspectbase):
            if aspect.language not in self.languages:
                return False

        for item in self:
            if issubaspect(aspect, item):
                return aspect not in self.exclude
        return False

    def get(self, aspect):
        """
        Return first item that match or contain an aspect. See
        :meth:`coalib.bearlib.aspects.aspectbase.get` for further example.

        :param aspect: An aspectclass OR name of an aspect.
        :return:       An aspectclass OR aspectclass instance, depend on
                       AspectList content. Return None if no match found.
        """
        if not isaspect(aspect):
            aspect = coalib.bearlib.aspects[aspect]
        if aspect in self.exclude:
            return None
        try:
            return next(filter(None, (item.get(aspect) for item in self)))
        except StopIteration:
            return None

    def _remove(self, item):
        """
        Remove first matching item in list.

        :param item:        An aspectclass
        :raises ValueError: When to be removed item is not found in list.
        """
        for aspect in self:
            if aspect is item or isinstance(aspect, item):
                return super().remove(aspect)

        raise ValueError('{}._remove(x): {} not in list.'
                         .format(type(self).__name__, item))

    def get_leaf_aspects(self):
        """
        Breakdown all of item in self into their leaf subaspects.

        :return: An AspectList contain ONLY leaf aspects.
        """
        aspects = type(self)()
        for leaf_aspect in itertools.chain.from_iterable([
                aspect.get_leaf_aspects() for aspect in self]):
            # Make sure no duplication
            if leaf_aspect not in aspects:
                aspects.append(leaf_aspect)

        for excluded_aspect in itertools.chain.from_iterable(
                [aspect.get_leaf_aspects() for aspect in self.exclude]):
            try:
                aspects._remove(excluded_aspect)
            except ValueError:
                continue

        return aspects
