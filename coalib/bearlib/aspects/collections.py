from coalib.bearlib.aspects import aspectclass, aspectbase
from coalib.bearlib.aspects.meta import issubaspect


class aspectlist(list):
    """
    List-derived container to hold aspects.
    """

    def __init__(self, seq=()):
        for item in seq:
            if not isinstance(item, (aspectclass, aspectbase)):
                raise TypeError(
                    '{} is not an aspectclass or an instance of an '
                    'aspectclass'.format(repr(item)))
        list.__init__(self, seq)

    def __contains__(self, aspect):
        for item in self:
            if issubaspect(aspect, item):
                return True
        return False
