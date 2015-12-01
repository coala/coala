from coalib.misc.Decorators import generate_eq, generate_repr


@generate_repr()
@generate_eq("documentation", "docstyle", "range")
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
        :param range:         The position range as a pair `(start, stop)`
                              where the documentation was found.
        """
        self.documentation = documentation
        self.docstyle = docstyle
        self.range = range

    def __str__(self):
        return self.documentation
