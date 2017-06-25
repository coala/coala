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
