import re

from coalib.bearlib.languages.documentation.DocstyleDefinition import (
    DocstyleDefinition)
from coalib.bearlib.languages.documentation.DocumentationComment import (
    DocumentationComment)
from coalib.results.TextRange import TextRange


def _extract_doc_comment_simple(content, line, column, markers):
    """
    Extract a documentation that starts at given beginning with simple layout.

    The property of the simple layout is that there's no each-line marker. This
    applies e.g. for python docstrings.

    :param content: Presplitted lines of the source-code-string.
    :param line:    Line where the documentation comment starts (behind the
                    start marker). Zero-based.
    :param column:  Column where the documentation comment starts (behind the
                    start marker). Zero-based.
    :param markers: The documentation identifying markers.
    :return:        If the comment matched layout a triple with end-of-comment
                    line, column and the extracted documentation. If not
                    matched, returns None.
    """
    align_column = column - len(markers[0])

    pos = content[line].find(markers[2], column)
    if pos != -1:
        return line, pos + len(markers[2]), content[line][column:pos]

    doc_comment = content[line][column:]
    line += 1

    while line < len(content):
        pos = content[line].find(markers[2])
        if pos == -1:
            doc_comment += ("\n" if content[line][align_column:] == ""
                            else content[line][align_column:])
        else:
            doc_comment += content[line][align_column:pos]
            return line, pos + len(markers[2]), doc_comment

        line += 1

    return None


def _extract_doc_comment_continuous(content, line, column, markers):
    """
    Extract a documentation that starts at given beginning with continuous
    layout.

    The property of the continuous layout is that the each-line-marker and the
    end-marker do equal. Documentation is extracted until no further marker is
    found. Applies e.g. for doxygen style python documentation:

    ```
    ## main
    #
    #  detailed
    ```

    :param content: Presplitted lines of the source-code-string.
    :param line:    Line where the documentation comment starts (behind the
                    start marker). Zero-based.
    :param column:  Column where the documentation comment starts (behind the
                    start marker). Zero-based.
    :param markers: The documentation identifying markers.
    :return:        If the comment matched layout a triple with end-of-comment
                    line, column and the extracted documentation. If not
                    matched, returns None.
    """
    marker_len = len(markers[1])

    doc_comment = content[line][column:]
    line += 1
    while line < len(content):
        pos = content[line].find(markers[1])
        if pos == -1:
            return line, 0, doc_comment
        else:
            doc_comment += content[line][pos + marker_len:]

        line += 1

    if content[line - 1][-1] == "\n":
        column = 0
    else:
        # This case can appear on end-of-document without a ``\n``.
        line -= 1
        column = len(content[line])

    return line, column, doc_comment


def _extract_doc_comment_standard(content, line, column, markers):
    """
    Extract a documentation that starts at given beginning with standard
    layout.

    The standard layout applies e.g. for C doxygen-style documentation:

    ```
    /**
     * documentation
     */
    ```

    :param content: Presplitted lines of the source-code-string.
    :param line:    Line where the documentation comment starts (behind the
                    start marker). Zero-based.
    :param column:  Column where the documentation comment starts (behind the
                    start marker). Zero-based.
    :param markers: The documentation identifying markers.
    :return:        If the comment matched layout a triple with end-of-comment
                    line, column and the extracted documentation. If not
                    matched, returns None.
    """
    pos = content[line].find(markers[2], column)
    if pos != -1:
        return line, pos + len(markers[2]), content[line][column:pos]

    doc_comment = content[line][column:]
    line += 1

    while line < len(content):
        pos = content[line].find(markers[2])
        each_line_pos = content[line].find(markers[1])

        if pos == -1:
            if each_line_pos == -1:
                # If the first text occurrence is not the each-line marker
                # now we violate the doc-comment layout.
                return None
            doc_comment += content[line][each_line_pos + len(markers[1]):]
        else:
            # If no each-line marker found or it's located past the end marker:
            # extract no further and end the doc-comment.
            if each_line_pos != -1 and each_line_pos + 1 < pos:
                doc_comment += content[line][each_line_pos +
                                             len(markers[1]):pos]

            return line, pos + len(markers[2]), doc_comment

        line += 1

    return None


def _extract_doc_comment(content, line, column, markers):
    """
    Delegates depending on the given markers to the right extraction method.

    :param content: Presplitted lines of the source-code-string.
    :param line:    Line where the documentation comment starts (behind the
                    start marker). Zero-based.
    :param column:  Column where the documentation comment starts (behind the
                    start marker). Zero-based.
    :param markers: The documentation identifying markers.
    :return:        If the comment matched layout a triple with end-of-comment
                    line, column and the extracted documentation. If not
                    matched, returns None.
    """
    if markers[1] == "":
        # Extract and align to start marker.
        return _extract_doc_comment_simple(content, line, column, markers)
    elif markers[1] == markers[2]:
        # Search for the each-line marker until it runs out.
        return _extract_doc_comment_continuous(content, line, column, markers)
    else:
        return _extract_doc_comment_standard(content, line, column, markers)


def _compile_multi_match_regex(strings):
    """
    Compiles a regex object that matches each of the given strings.

    :param strings: The strings to match.
    :return:        A regex object.
    """
    return re.compile("|".join(re.escape(s) for s in strings))


def _extract_doc_comment_from_line(content, line, column, regex,
                                   marker_dict, docstyle_definition):
    cur_line = content[line]
    begin_match = regex.search(cur_line, column)
    if begin_match:
        indent = cur_line[:begin_match.start()]
        column = begin_match.end()
        for marker in marker_dict[begin_match.group()]:
            doc_comment = _extract_doc_comment(content, line, column, marker)
            if doc_comment is not None:
                end_line, end_column, documentation = doc_comment

                rng = TextRange.from_values(line + 1,
                                            begin_match.start() + 1,
                                            end_line + 1,
                                            end_column + 1)
                doc = DocumentationComment(documentation, docstyle_definition,
                                           indent, marker, rng)

                return end_line, end_column, doc

    return line + 1, 0, None


def extract_documentation_with_markers(content, docstyle_definition):
    """
    Extracts all documentation texts inside the given source-code-string.

    :param content: The source-code-string where to extract documentation from.
                    Needs to be a list or tuple where each string item is a
                    single line (including ending whitespaces like ``\\n``).
    :param markers: The list/tuple of marker-sets that identify a
                    documentation-comment. Low-index markers have higher
                    priority than high-index markers.
    :return:        An iterator returning each DocumentationComment found in
                    the content.
    """
    # Prepare marker-tuple dict that maps a begin pattern to the corresponding
    # marker_set(s). This makes it faster to retrieve a marker-set from a
    # begin sequence we initially want to search for in source code. Then
    # the possible found documentation match is processed further with the
    # rest markers.
    markers = docstyle_definition.markers

    marker_dict = {}
    for marker_set in markers:
        if marker_set[0] not in marker_dict:
            marker_dict[marker_set[0]] = [marker_set]
        else:
            marker_dict[marker_set[0]].append(marker_set)

    # Using regexes to perform a variable match is faster than finding each
    # substring with ``str.find()`` choosing the lowest match.
    begin_regex = _compile_multi_match_regex(
        marker_set[0] for marker_set in markers)

    line = 0
    column = 0
    while line < len(content):
        line, column, doc = _extract_doc_comment_from_line(
            content,
            line,
            column,
            begin_regex,
            marker_dict,
            docstyle_definition)
        if doc:
            yield doc


def extract_documentation(content, language, docstyle):
    """
    Extracts all documentation texts inside the given source-code-string using
    the coala docstyle definition files.

    The documentation texts are sorted by their order appearing in ``content``.

    For more information about how documentation comments are identified and
    extracted, see DocstyleDefinition.doctypes enumeration.

    :param content:            The source-code-string where to extract
                               documentation from. Needs to be a list or tuple
                               where each string item is a single line
                               (including ending whitespaces like ``\\n``).
    :param language:           The programming language used.
    :param docstyle:           The documentation style/tool used
                               (e.g. doxygen).
    :raises FileNotFoundError: Raised when the docstyle definition file was not
                               found.
    :raises KeyError:          Raised when the given language is not defined in
                               given docstyle.
    :raises ValueError:        Raised when a docstyle definition setting has an
                               invalid format.
    :return:                   An iterator returning each DocumentationComment
                               found in the content.
    """
    docstyle_definition = DocstyleDefinition.load(language, docstyle)
    return extract_documentation_with_markers(content, docstyle_definition)
