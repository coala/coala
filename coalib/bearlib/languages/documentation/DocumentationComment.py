from coala_decorators.decorators import generate_eq, generate_repr


@generate_repr()
@generate_eq("documentation", "language", "docstyle",
             "indent", "marker", "range")
class DocumentationComment:
    """
    The DocumentationComment holds information about a documentation comment
    inside source-code, like position etc.
    """

    def __init__(self, documentation, language,
                 docstyle, indent, marker, range):
        """
        Instantiates a new DocumentationComment.

        :param documentation: The documentation text.
        :param language:      The language of the documention.
        :param docstyle:      The docstyle used in the documentation.
        :param indent:        The string of indentation used in front
                              of the first marker of the documentation.
        :param marker:        The three-element tuple with marker strings,
                              that identified this documentation comment.
        :param range:         The position range of type TextRange.
        """
        self.documentation = documentation
        self.language = language.lower()
        self.docstyle = docstyle.lower()
        self.indent = indent
        self.marker = marker
        self.range = range

    def __str__(self):
        return self.documentation
