from coala_decorators.decorators import generate_eq, generate_repr


@generate_repr()
@generate_eq("documentation", "marker", "range")
class DocumentationComment:
    """
    The DocumentationComment holds information about a documentation comment
    inside source-code, like position etc.
    """

    def __init__(self, documentation, marker, range):
        """
        Instantiates a new DocumentationComment.

        :param documentation: The documentation text.
        :param marker:        The three-element tuple with marker strings that
                              identified this documentation comment.
        :param range:         The position range of type TextRange.
        """
        self.documentation = documentation
        self.marker = marker
        self.range = range

    def __str__(self):
        return self.documentation
