import re

from coalib.bearlib.languages.documentation.DocstyleDefinition import (
    DocstyleDefinition)
from coalib.bearlib.languages.documentation.DocumentationComment import (
    DocumentationComment)
from coalib.results.TextRange import TextRange


# Used to break out of outer loops via exception raise.
class _BreakOut(Exception):
    pass


def _compile_multi_match_regex(strings):
    """
    Compiles a regex object that matches each of the given strings.

    :param strings: The strings to match.
    :return:        A regex object.
    """
    return re.compile("|".join(re.escape(s) for s in strings))


def extract_documentation_with_docstyle(content, docstyle_definition):
    """
    Extracts all documentation texts inside the given source-code-string.

    :param content:             The source-code-string where to extract
                                documentation from or an iterable with strings
                                where each string is a single line (including
                                ending whitespaces like `\\n`).
    :param docstyle_definition: The DocstyleDefinition that identifies the
                                documentation comments.
    :return:                    An iterator returning each documentation text
                                found in the content.
    """
    if isinstance(content, str):
        content = content.splitlines(keepends=True)
    else:
        content = list(content)

    # Prepare marker-tuple dict that maps a begin pattern to the corresponding
    # marker_set(s). This makes it faster to retrieve a marker-set from a
    # begin sequence we initially want to search for in source code. Then
    # the possible found documentation match is processed further with the
    # rest markers.
    begin_sequence_dict = {}
    for marker_set in docstyle_definition.markers:
        if marker_set[0] not in begin_sequence_dict:
            begin_sequence_dict[marker_set[0]] = [marker_set]
        else:
            begin_sequence_dict[marker_set[0]].append(marker_set)

    # Using regexes to perform a variable match is faster than finding each
    # substring with `str.find()` choosing the lowest match.
    begin_regex = _compile_multi_match_regex(
        marker_set[0] for marker_set in docstyle_definition.markers)

    line = 0
    line_pos = 0
    while line < len(content):
        begin_match = begin_regex.search(content[line], line_pos)

        if begin_match:
            begin_match_line = line
            # Prevents infinite loop when the start marker matches but not the
            # complete documentation comment.
            line_pos = begin_match.end()

            # begin_sequence_dict[begin_match.group()] returns the marker set
            # the begin sequence from before matched.
            for marker_set in begin_sequence_dict[begin_match.group()]:
                try:
                    # If the each-line marker and the end marker do equal,
                    # search for the each-line marker until it runs out.
                    if marker_set[1] == marker_set[2]:
                        docstring = content[line][begin_match.end():]

                        line2 = line + 1
                        stripped_content = content[line2].lstrip()

                        # Now the each-line marker is no requirement for a
                        # docstring any more, just extract as long as there are
                        # no each-line markers any more.
                        while (stripped_content[:len(marker_set[1])] ==
                               marker_set[1]):
                            docstring += stripped_content[len(marker_set[1]):]

                            line2 += 1
                            if line2 >= len(content):
                                # End of content reached, done with
                                # doc-extraction.
                                break

                            stripped_content = content[line2].lstrip()

                        line = line2 - 1
                        line_pos = len(content[line])
                    else:
                        end_marker_pos = content[line].find(marker_set[2],
                                                            begin_match.end())

                        if end_marker_pos == -1:
                            docstring = content[line][begin_match.end():]

                            line2 = line + 1
                            if line2 >= len(content):
                                continue

                            end_marker_pos = content[line2].find(marker_set[2])

                            while end_marker_pos == -1:
                                if marker_set[1] == "":
                                    # When no each-line marker is set (i.e. for
                                    # Python docstrings), then align the
                                    # comment to the start-marker.
                                    stripped_content = (
                                        content[line2][begin_match.start():])
                                else:
                                    # Check whether we violate the each-line
                                    # marker "rule".
                                    current_each_line_marker = (content[line2]
                                        [begin_match.start():
                                         begin_match.start()
                                             + len(marker_set[1])])
                                    if (current_each_line_marker !=
                                            marker_set[1]):
                                        # Effectively a 'continue' for the
                                        # outer for-loop.
                                        raise _BreakOut

                                    stripped_content = (
                                        content[line2][begin_match.start()
                                                       + len(marker_set[1]):])

                                docstring += stripped_content
                                line2 += 1

                                if line2 >= len(content):
                                    # End of content reached, so there's no
                                    # closing marker and that's a mismatch.
                                    raise _BreakOut

                                end_marker_pos = content[line2].find(
                                    marker_set[2])

                            docstring += (content[line2]
                                [begin_match.start():end_marker_pos])
                            line = line2
                        else:
                            docstring = (content[line]
                                [begin_match.end():end_marker_pos])

                        line_pos = end_marker_pos + len(marker_set[2])

                    rng = TextRange.from_values(begin_match_line + 1,
                                                begin_match.start() + 1,
                                                line + 1,
                                                line_pos + 1)

                    yield DocumentationComment(docstring,
                                               docstyle_definition,
                                               marker_set,
                                               rng)

                    break

                except _BreakOut:
                    # Continues the marker_set loop.
                    pass

        else:
            line += 1
            line_pos = 0


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
    docstyle_definition = DocstyleDefinition.load(language, docstyle)
    return extract_documentation_with_docstyle(content, docstyle_definition)
