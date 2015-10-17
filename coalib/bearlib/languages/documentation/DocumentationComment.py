from coalib.misc.Decorators import generate_repr


@generate_repr()
class DocumentationComment:
    """
    The DocumentationComment holds information about a documentation comment
    inside source-code, like position, docstyle etc.
    """

    def __init__(self, documentation, docstyle, range):
        """
        Instantiates a new DocumentationComment.

        :param documentation: The documentation text.
        :param docstyle:      The DocstyleDefinition.
        :param range:         The range as a pair (start, stop) where the
                              documentation was found.
        """
        self.documentation = documentation
        self.docstyle = docstyle
        self.range = range

    def __str__(self):
        return self.documentation

    def __eq__(self, other):
        return (other is not None and
                self.documentation == other.documentation and
                self.docstyle == other.docstyle and
                self.range == other.range)
