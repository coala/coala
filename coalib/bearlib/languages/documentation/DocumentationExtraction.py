from operator import attrgetter

from coalib.bearlib.languages.documentation.DocstyleDefinition import (
    DocstyleDefinition,
    DOCTYPES)
from coalib.bearlib.languages.documentation.DocumentationComment import (
    DocumentationComment)
from coalib.parsing.StringProcessing import search_in_between


def _extract_documentation_standard(content,
                                    marker_start,
                                    marker_eachline,
                                    marker_stop):
    """
    Extract documentation of doctype 'standard'.

    :param content:         The source-code-string where to extract
                            documentation from.
    :param marker_start:    The start marker.
    :param marker_eachline: The each-line marker.
    :param marker_stop:     The stop marker.
    :return:                An iterator yielding a tuple where the first entry
                            is a range pair (start, end) describing the range
                            where the documentation was found and the second
                            one the actual documentation string.
    """

    for match in search_in_between(marker_start, marker_stop, content):
        it = iter(str(match.inside).splitlines(keepends=True))
        docstring = next(it)
        docstring += "".join(line.lstrip(" \t").replace(marker_eachline, "", 1)
                             for line in it)

        yield ((match.begin.position, match.end.end_position), docstring)


"""
Contains all registered documentation extraction functions.

The functions must at least accept one parameter, the source-code-content
where to extract documentation from. They have to yield tuples where the first
entry is the SourcePosition and the second one the actual documentation string.
"""
_extract = {DOCTYPES.standard : _extract_documentation_standard}


def extract_documentation_with_docstyle(content, docstyle_definition):
    """
    Extracts all documentation texts inside the given source-code-string.

    For more information about how documentation comments are identified and
    extracted, see DocstyleDefinition.doctypes enumeration.

    :param content:             The source-code-string where to extract
                                documentation from.
    :param docstyle_definition: The DocstyleDefinition that identifies the
                                documentation comments.
    :raises ValueError:         Raised when the docstyle definition markers
                                have an invalid format.
    :return:                    An iterator returning each documentation text
                                found in the content.
    """
    markers = docstyle_definition.markers

    try:
        results = _extract[docstyle_definition.doctype](content, *markers)

        # We want to check whether we invoke everything correctly when
        # unpacking markers, so let this routine be the generator that yields
        # the results and the actual function return the generator so the
        # initial part is executed.
        def extract_documentation_with_docstyle_generator():
            for result in results:
                yield DocumentationComment(result[1],
                                           docstyle_definition,
                                           result[0])

        return extract_documentation_with_docstyle_generator()

    except TypeError:
        raise ValueError(
            "Docstyle-setting for language {} defined in docstyle {} for "
            "doctype {} has an invalid format. For more information about "
            "documentation marker settings see `DocstyleDefinition` object."
            .format(repr(docstyle_definition.language),
                    repr(docstyle_definition.docstyle),
                    repr(docstyle_definition.doctype)))


def extract_documentation(content, language, docstyle):
    """
    Extracts all documentation texts inside the given source-code-string using
    the coala docstyle definition files.

    The documentation texts are sorted by their order appearing in `content`.

    For more information about how documentation comments are identified and
    extracted, see DocstyleDefinition.doctypes enumeration.

    :param content:            The source-code-string where to extract
                               documentation from.
    :param language:           The programming language used.
    :param docstyle:           The documentation style/tool used
                               (i.e. doxygen).
    :raises FileNotFoundError: Raised when the docstyle definition file was not
                               found.
    :raises KeyError:          Raised when the given language is not defined in
                               given docstyle.
    :raises ValueError:        Raised when a docstyle definition setting has an
                               invalid format.
    :return:                   An iterator returning each DocumentationComment
                               found in the content.
    """
    docstyle_definitions = DocstyleDefinition.load(language, docstyle)

    def get_chained_results():
        for definition in docstyle_definitions:
            results = extract_documentation_with_docstyle(content, definition)
            # Don't turn this into a 'return' statement, because we want to
            # yield every result from every definition inside this loop.
            for result in results:
                yield result

    # The sort compares the range pairs, since tuples support comparison. Even
    # it will never happen two compare the second entry (the range
    # end-position), it enhances our sort.
    return sorted(get_chained_results(), key=attrgetter("range"))
