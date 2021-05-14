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
            joined_names = ' -> '.join(names)
            msg = f'Circular dependency detected: {joined_names}'
        else:
            msg = 'Circular dependency detected.'
        super().__init__(msg)
