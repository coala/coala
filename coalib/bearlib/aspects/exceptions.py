class AspectTypeError(TypeError):
    """
    This error is raised when an object is not an ``aspectclass`` or an
    instance of ``aspectclass``
    """

    def __init__(self, item):
        self.item = item
        message = ('{} is not an aspectclass or an instance of an '
                   'aspectclass'.format(repr(self.item)))
        super().__init__(message)


class AspectLookupError(LookupError):
    """
    Error raised when trying to search aspect.
    """

    def __init__(self, aspectname, message=None):
        self.aspectname = aspectname
        if message is None:
            message = ('Error when trying to search aspect named {}'
                       .format(repr(aspectname)))
        super().__init__(message)


class AspectNotFoundError(AspectLookupError):
    """
    No aspect found.
    """

    def __init__(self, aspectname):
        message = ('No aspect named {}'.format(repr(aspectname)))
        super().__init__(aspectname, message)


class MultipleAspectFoundError(AspectLookupError):
    """
    Multiple aspect are found.
    """

    def __init__(self, aspectname, other_aspects):
        self.other_aspects = other_aspects
        message = ('Multiple aspects named {}. Choose from {}'.format(
            repr(aspectname),
            repr(sorted(other_aspects, key=lambda a: a.__qualname__))))
        super().__init__(aspectname, message)
