from itertools import chain
from operator import attrgetter

from coalib.bearlib.languages.documentation.DocstyleDefinition import (
    DocstyleDefinition)
from coalib.bearlib.languages.documentation.DocumentationComment import (
    DocumentationComment)


"""
Contains all registered documentation extraction functions.

The functions must at least accept one parameter, the source-code-content
where to extract documentation from. They have to yield tuples where the first
entry is the `(start, stop)`-position tuple and the second one the actual
documentation string.
"""
_extract = {}


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
                               found. This is a compatability exception from
                               `coalib.misc.Compatability` module.
    :raises KeyError:          Raised when the given language is not defined in
                               given docstyle.
    :raises ValueError:        Raised when a docstyle definition setting has an
                               invalid format.
    :return:                   An iterator returning each DocumentationComment
                               found in the content.
    """
    docstyle_definitions = DocstyleDefinition.load(language, docstyle)

    chained = chain(*(extract_documentation_with_docstyle(content, definition)
                      for definition in docstyle_definitions))
    return sorted(chained, key=attrgetter("range"))
