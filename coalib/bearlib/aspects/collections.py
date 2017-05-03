from coalib.bearlib.aspects.meta import issubaspect, assert_aspect
from inspect import isclass


class aspectlist(list):
    """
    List-derived container to hold aspects.
    """

    def __init__(self, seq=(), bear=None):
        super().__init__(map(assert_aspect, seq))
        self.bear = bear

    def __contains__(self, aspect):
        if self.bear is not None and not isclass(aspect):
            for language in self.bear.languages:
                if type(aspect.language) is type(language):
                    break
            else:
                return False
        for item in self:
            if issubaspect(aspect, item):
                return True
        return False
