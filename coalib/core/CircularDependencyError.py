class CircularDependencyError(Exception):
    """
    An error identifying a circular dependency.
    """

    def __init__(self, node=None):
        """
        Creates the CircularDependencyError with a helpful message about the
        dependency.

        :param node:
            The node that was encountered twice and closes the dependency
            circle.
        """
        message = 'Circular dependency detected.'
        if node is not None:
            message += ' {0!r} -> ... -> {0!r}'.format(node)

        Exception.__init__(self, message)
