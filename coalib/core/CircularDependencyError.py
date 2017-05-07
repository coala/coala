class CircularDependencyError(RuntimeError):
    """
    An error identifying a circular dependency.
    """

    def __init__(self, names=None):
        """
        Creates the CircularDependencyError with a helpful message about the
        dependency.

        :param names:
            The names of the nodes that form a dependency circle.
        """
        if names:
            msg = 'Circular dependency detected: {names}'.format(
                names=' -> '.join(names))
        else:
            msg = 'Circular dependency detected.'
        super().__init__(msg)
