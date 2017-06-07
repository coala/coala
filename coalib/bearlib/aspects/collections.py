from coalib.bearlib.aspects.meta import issubaspect, assert_aspect


class aspectlist(list):
    """
    List-derived container to hold aspects.
    """

    def __init__(self, seq=()):
        super().__init__(map(assert_aspect, seq))

    def __contains__(self, aspect):
        for item in self:
            if issubaspect(aspect, item):
                return True
        return False
