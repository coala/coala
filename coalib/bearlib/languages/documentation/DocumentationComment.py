from coalib.misc.Decorators import generate_eq, generate_repr


@generate_repr()
@generate_eq("documentation", "docstyle", "marker", "range")
class DocumentationComment:
    """
    The DocumentationComment holds information about a documentation comment
    inside source-code, like position, docstyle etc.
    """

    def __init__(self, documentation, docstyle, marker, range):
        """
        Instantiates a new DocumentationComment.

        :param documentation: The documentation text.
        :param docstyle:      The DocstyleDefinition.
        :param marker:        The specific set of marker strings that
                              identified this documentation comment.
        :param range:         The position range of type TextRange.
        """
        self.documentation = documentation
        self.docstyle = docstyle
        self.marker = marker
        self.range = range

    def __str__(self):
        return self.documentation
