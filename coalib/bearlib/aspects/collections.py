import coalib.bearlib.aspects
from coalib.bearlib.aspects.meta import isaspect, issubaspect


class AspectList(list):
    """
    List-derived container to hold aspects.
    """

    def __init__(self, seq=()):
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
        """
        super().__init__((item if isaspect(item) else
                          coalib.bearlib.aspects[item] for item in seq))

    def __contains__(self, aspect):
        for item in self:
            if issubaspect(aspect, item):
                return True
        return False
