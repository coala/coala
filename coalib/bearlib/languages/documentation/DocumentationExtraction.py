"""
Language and docstyle independent extraction of documenation comments.

Each of the functions is built upon one another, and at the last,
exposes a single function :func:`extract_documentation_with_markers`
which is used by :class:`.DocBaseClass`, to extract documentation.
"""

import re

from coalib.bearlib.languages.documentation.DocumentationComment import (
    DocumentationComment, MalformedComment)
from coalib.results.TextPosition import TextPosition
from coalib.results.TextRange import TextRange
from textwrap import dedent


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
            line_column = len(content[line])-len(content[line].lstrip())
            doc_comment += ('\n' if content[line][align_column:] == ''
                            else content[line].strip()+'\n'
                            if line_column < align_column
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
    found. Applies e.g. for doxygen style python documentation::

        ## main
        #
        #  detailed

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

    if content[line - 1][-1] == '\n':
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

    The standard layout applies e.g. for C doxygen-style documentation::

        /**
         * documentation
         */

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
    if markers[1] == '':
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
    return re.compile('|'.join(re.escape(s) for s in strings))


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

                position = TextPosition(line + 1, len(indent) + 1)
                doc = DocumentationComment(documentation, docstyle_definition,
                                           indent, marker, position)

                break

        if doc_comment:
            return end_line, end_column, doc
        else:
            malformed_comment = MalformedComment(dedent("""\
                Please check the docstring for faulty markers. A starting
                marker has been found, but no instance of DocComment is
                returned."""), line)
            return line + 1, 0, malformed_comment

    return line + 1, 0, None


def extract_documentation_with_markers(content, docstyle_definition):
    """
    Extracts all documentation texts inside the given source-code-string.

    :param content:
        The source-code-string where to extract documentation from.
        Needs to be a list or tuple where each string item is a single
        line (including ending whitespaces like ``\\n``).
    :param docstyle_definition:
        The ``DocstyleDefinition`` instance that defines what docstyle is
        being used in the documentation.
    :return:
        An iterator returning each DocumentationComment found in the content.
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

        if doc and isinstance(doc, MalformedComment):
            yield doc
        elif doc:
            # Ignore string literals
            ignore_regex = re.compile(
                '^\s*r?(?P<marker>' +
                ('|'.join(re.escape(s) for s in doc.marker[0])) +
                ')')
            # Starting line of doc_string where marker is present
            start_line = doc.range.start.line - 1
            ignore_string_match = ignore_regex.search(content[start_line])

            # Instantiate padding
            top_padding = 0
            bottom_padding = 0
            # minus 2 because we want to check the line before the marker.
            start_index = doc.range.start.line - 2
            end_index = doc.range.end.line
            while start_index >= 0 and not content[start_index].strip():
                top_padding += 1
                start_index -= 1
            # If the end_index is instantiated above the len(content) i.e.
            # In case where ending marker of docstring is at the last line.
            # Then the doc.bottom_padding will be default to 0. This will also
            # prevent IndexError raised by content[end_index].
            while end_index < len(content) and not content[end_index].strip():
                # This condition will take place if theres an inline docstring
                # following documentation.
                if ((doc.marker[2]+'\n') != content[end_index-1][-4:]
                        and bottom_padding == 0):
                    break
                bottom_padding += 1
                end_index += 1

            class_regex = re.compile(
                doc.docstyle_definition.docstring_type_regex.class_sign)
            function_regex = re.compile(
                doc.docstyle_definition.docstring_type_regex.func_sign)

            # End line differs when mid marker and end marker is different
            if doc.marker[1] == doc.marker[2]:
                end_index = end_index - 1

            # Check for docstring_position and then check for class regex
            # and function regex to define the type of docstring.
            if doc.docstyle_definition.docstring_position == 'top':
                if class_regex.search(content[start_index]):
                    doc.docstring_type = 'class'
                elif function_regex.search(content[start_index]):
                    doc.docstring_type = 'function'
            elif doc.docstyle_definition.docstring_position == 'bottom':
                if (end_index < len(content) and
                        class_regex.search(content[end_index])):
                    doc.docstring_type = 'class'
                elif (end_index < len(content) and
                        function_regex.search(content[end_index])):
                    doc.docstring_type = 'function'

            # Disabled automatic padding for docstring_type='others' as this
            # will cause overlapping of range in consecutive docstrings. Which
            # diff.replace() is unable to handle.
            if doc.docstring_type != 'others':
                doc.top_padding = top_padding
                doc.bottom_padding = bottom_padding

                doc.range = TextRange.from_values(
                    start_index + 2,
                    1 if top_padding > 0 else doc.range.start.column,
                    end_index,
                    1 if bottom_padding > 0 else doc.range.end.column)

            if ignore_string_match:
                yield doc
