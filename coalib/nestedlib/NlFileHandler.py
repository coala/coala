from coalib.io.File import File
from copy import deepcopy
import logging

# This is used to combine the nl_sections of a mixed language line produced by
# a parser  into a single nl_section.
PARSER_MIXED_LINE_COMB = [{'PyJinjaParser': 'jinja2'}]


def get_nl_sections(all_nl_sections, lang):
    """
    Get the nl_section of a particular language from all the nl_sections of the
    file. And sort the nl_section according to their index.

    When the parser parses the file, it returns a list of nl_section containing
    all the nested language. In order to make a file_dict, only the sections
    belonging to one language is needed.

    :param all_nl_sections: The list of nl_sections the parser ouputs
    :param lang:            The language whose nl_section is needed.
    """
    # Get nl_section of `lang` language
    nl_sections = []
    for nl_section in all_nl_sections:
        if nl_section.language == lang:
            nl_sections.append(nl_section)

    # Sort the nl_sections according to their indices
    nl_sections = sorted(nl_sections, key=lambda nl_section: nl_section.index)
    return nl_sections


def get_line_list(nl_sections, orig_file_path):
    """
    Create a list of lines that would be present in the temporary file.

    From the nl_sections, get the information of start and end and use this to
    get the content at those positions.

    :param nl_sections:     The nl_sections belonging to one language
    :param orig_file_path:  The absolute path of the original nested file.
    """
    file = File(orig_file_path)

    # Initialiaze a line_list with whitespace. The lenght of this list will
    # be equal to the number of lines in the actual files.
    # The index of the list points to the line number of the original file.
    # The means line_list[3] contains the line at line number 4 of the original
    # file.
    line_list = []
    line_list = [' ' for index in range(0, file.__len__())]

    for nl_section in nl_sections:

        start_line = nl_section.start.line
        start_column = nl_section.start.column
        end_line = nl_section.end.line
        end_column = nl_section.end.column

        for line_nr in range(start_line, end_line+1):

            # Make the length of line equal to the length of original line
            if(line_list[line_nr-1].isspace()):
                line_list[line_nr-1] = ' '*len(file[line_nr-1])

            orig_line = file[line_nr-1]
            end_orig_line = len(orig_line)-1
            line = line_list[line_nr-1]

            # If the section contains only one line.
            # This case generally happens for mixed lang line
            if (line_nr == start_line and line_nr == end_line):

                # If column is not mentioned, then it means that the entire line
                # is present in the section.
                if (not end_column) or (not start_column):
                    line_list[line_nr-1] = orig_line

                else:
                    # section_content stores the part of the line that belongs
                    # to the section.
                    section_content = file[line_nr -
                                           1][start_column-1:end_column]

                    if(start_column-1 > 0) and (end_column < end_orig_line):
                        line_list[line_nr-1] = (line[0:start_column-1] +
                                                section_content +
                                                line[end_column:end_orig_line])

                    elif(start_column-1 == 0) and (end_column < end_orig_line):
                        line_list[line_nr-1] = (section_content +
                                                line[end_column:end_orig_line])

                    elif(start_column-1 > 0) and (end_column == end_orig_line):
                        line_list[line_nr-1] = (line[0:start_column-1] +
                                                section_content)
                    else:
                        line_list[line_nr-1] = section_content

            elif (line_nr == start_line):
                line_list[line_nr-1] = orig_line

            elif (line_nr == end_line):
                if(end_column == len(orig_line)-1):
                    line_list[line_nr-1] = orig_line
                else:
                    line_list[line_nr-1] = (orig_line[0:end_column-1] +
                                            line[end_column-1:end_orig_line])

            else:
                line_list[line_nr-1] = orig_line
    return line_list


def beautify_line_list(line_list):
    """
    Beautify the line list.

    It add a newline character at the end of items if newline character is not
    not present and also adds a newline character if the item is only
    space. Because those line might have been either a pure line or an empty
    line.

    :param line_list: The list containing all the lines of temporary file.
    :return:          The beautified tuple containing all the lines.

    >>> line_list = ['', '\\n','asdas adasd', 'asdasdawq12\\n']
    >>> beautify_line_list(line_list)
    ('\\n', '\\n', 'asdas adasd\\n', 'asdasdawq12\\n')

    """
    for i, line in enumerate(line_list):
        if not line.strip():
            line_list[i] = '\n'
        elif line[-1] == '\n':
            continue
        else:
            line_list[i] += '\n'

    return(tuple(line_list))


def is_mixed_lang_section(all_nl_sections, nl_section_to_check):
    """
    Check if the nl_section is a part of mixed nl_section.

    Note that, every mixed_nl_line was divided into a seperate nl_section.
    They were/are not suppsed to be mixed with pure_language lines. So we
    can find the mixed_nl_section, if we find that there are more than one
    nl_section that same start_line and end_line.

    We return the number of nl_sections present on the line, so that we can
    jump by that many sections, instead of checking them again and again.
    """
    start_line = nl_section_to_check.start.line

    all_nl_sections_line = [nl_section for nl_section in all_nl_sections
                            if nl_section.start.line == start_line]

    if (len(all_nl_sections_line) > 1):
        return True, len(all_nl_sections_line)

    return False, 0


def get_preprocessed_nl_sections(all_nl_sections, parser):
    """
    Preprocess the nl_sections.

    The parser converts the original nested language file into different
    nl_sections. During those conversion, we encounter two types of files,
    one pure lines and mixed language lines. The pure languages lines were
    grouped into one section and they were never appeneded with the the mixed
    language lines. The mixed languge lines were divided into various different
    nl_sections.

    This function converts the sections generated by the parser for the mixed
    language lines into a single section. We are doing this with an
    understanding that when two languages are nested, there is usually some form
    of depenedcy in each othere. In such cases, we are sure that atleast one of
    the bear writer would have written the bear such that it ignores the other
    language.

    For example: For a file that has both Jinja and Python nested. We can see
    that Jinja2Bear, lints only the jinja lines ignoring the python lines.
    We can make use of this functionality while linting. That means, we could
    pass the mixed language line to the Jinja2Bear which could lint the
    mixed language.

    The problem with the above approach is that in mixed_language lines only
    the jinja2 part will be linted and not python lines.

    NOTE: This is only a temporary solution. We could use this until we find
    how to lint the nl_section which are  of mixed language using the position
    markers.
    """
    # Get the language you want to mark the mixed_language lines with.
    # For eg: In a combination of Python and Jinja, we mark the mixed lang
    # nl_sections with jinja2 since Jinja2Bear can lint through them
    parser_name = parser.__class__.__name__
    mixed_lang = ''
    for parser_mixed_lang_dict in PARSER_MIXED_LINE_COMB:
        for parser, lang in parser_mixed_lang_dict.items():
            if parser_name.lower() == parser.lower():
                mixed_lang = lang
                break

    if not mixed_lang:
        logging.error('No PARSER_MIXED_LINE_COMB exist')
        raise SystemExit(2)

    preprocessed_nl_section_index = 1
    preprocess_nl_sections = []
    index = 0
    # Get new nl_section which aggregates the mixed_lang section into one.
    while(index < len(all_nl_sections)):

        nl_section = all_nl_sections[index]
        mixed_lang_section, num_mixed_nl_sections = is_mixed_lang_section(
                                            all_nl_sections[index:],
                                            nl_section_to_check=nl_section)
        if mixed_lang_section:
            mixed_nl_section = deepcopy(nl_section)
            mixed_nl_section.start.column = None
            mixed_nl_section.end.column = None
            mixed_nl_section.linted_start.column = None
            mixed_nl_section.linted_end.column = None
            mixed_nl_section.language = mixed_lang
            mixed_nl_section.index = preprocessed_nl_section_index

            preprocess_nl_sections.append(mixed_nl_section)

            # Since the current nl_section is a mixed section, there will surely
            # be few other another mixed_nl_sections below it. It's useless
            # num_mixed_nl_section also includes the current section
            index = index + (num_mixed_nl_sections)
            preprocessed_nl_section_index += 1

        else:
            pure_nl_section = deepcopy(nl_section)
            pure_nl_section.index = preprocessed_nl_section_index
            preprocess_nl_sections.append(pure_nl_section)
            preprocessed_nl_section_index += 1
            index += 1

    return preprocess_nl_sections


def preprocess_nl_line_list(nl_sections, lines_list, lang):
    """
    Add position markers to the line list to indicate the `start` and `end` of
    a Nested language section.
    This helps while retrieving the section from the linted file.

    For eg: Let's assume the following snippet is from a segregated Pyhton temp
    file from a Python-Jinja nested original file.
    file

    The following example:

    Let's assume we have the following file:
    x = "python lines"
    y = "Next 2 lines has jinja 2"


    z = "Next python nl_section starts"

    Assume the empty lines to be the lines where jinja2 content was present.

    After preprocessing the above lines looks like:
    >>> preprocessed_line_list = ['# Start nl section 1\\n',
    ...                           'x = "python lines"\\n',
    ...                           'y = "Next 2 lines has jinja 2"\\n',
    ...                           '# End nl section 1\\n',
    ...                           '\\n',
    ...                           '\\n',
    ...                           '# Start nl section 2\\n',
    ...                           'z = "Next python nl_section starts"\\n',
    ...                           '# End nl section 2\\n',
    ...                           ]

    We will also include the section number/index into the marker string.
    This helps while reassembling.
    Note that the lines where the nl section position markers are present would
    be ignored by coala.(Refer the ignore_ranges in process/Processing.py).
    This would remove the worry of they being linted and affecting the actual
    code.
    """

    # Add the prefix string according to the language combination.
    # For now this string works for the combination of Python and Jinja
    # When more language support is added, You can use `if` statements to
    # use the proper prefix
    start_marker_prefix = '# Start Nl Section: '
    end_marker_prefix = '# End Nl Section: '

    # Store the count of number of lines have been added.
    added_lines = 0

    for nl_section in nl_sections:
        index = nl_section.index

        # Insert the start position marker for the nl section
        start_pos = nl_section.start.line - 1
        start_pos_marker = start_pos + added_lines
        start_marker = start_marker_prefix + str(index)
        lines_list.insert(start_pos_marker, start_marker)
        added_lines += 1
        # linted_start maintains the position of the nl_section before it goes
        # to the bears
        nl_section.linted_start.line += added_lines

        # Insert the end position marker for the nl section
        end_pos = nl_section.end.line - 1
        end_pos_marker = (end_pos + added_lines) + 1
        end_marker = end_marker_prefix + str(index)
        lines_list.insert(end_pos_marker, end_marker)
        nl_section.linted_end.line += added_lines
        added_lines += 1

    return lines_list


def get_nl_file_dict(orig_file_path, temp_file_name, lang, parser):
    """
    Return a dictionary with `temp_file_name` as the key and the value as the
    tuple containing the lines the lines belonging to the param `lang`.

    :param orig_file_path: Path of the original nested file
    :param temp_file_name: Name of the temporary file that acts as the file
                           holder which consists of only the lines of the
                           `lang` language from the originianl nested file.
                           The temporary files  are said to be the pure
                           langauge files i.e the files that contains only one
                           programming language.
    :param lang:           Specifies the language of the line we want to extract
                           from the original file.
    :param parser:         The parser object to make nl_sections.

    Suppose we have the following file contents. And the name of file is
    `test.py`. Thie file contains both `python` and `jinja2` lines.

    >>> file_contents = ("for x in y:\\n",
    ...                  "{% if x is True %}\\n",
    ...                  "\\t{% set var3 = value3 %}\\n",
    ...                  "{% elif %}\\n",
    ...                  "\\t\\t{{ var }} = print('Bye Bye')\\n")


    The file_dict that contains only `jinja2` lines of the original files are:
    >>> jinja2_dict = {'test.py_nl_jinja2': ('\\n',
    ...                '{% if x is True %}\\n',
    ...                '    {% set var3 = value3 %}\\n',
    ...                '{% elif %}\\n',
    ...                '        {{ var }}                   \\n')}

    The file_dict that contains only `python` lines of the original file are:
    >>> python_dict = {'test.py_nl_python': ('for x in y:\\n',
    ...                '\\n',
    ...                '\\n',
    ...                '\\n',
    ...                "                  = print('Bye Bye')\\n")}
    """
    # ENHANCEMENT: Maybe instead of making parser parse through the file for
    # every nested language. We can store it somehow?
    all_nl_sections = parser.parse(orig_file_path)
    preprocessed_nl_sections = get_preprocessed_nl_sections(all_nl_sections,
                                                            parser)
    nl_sections = get_nl_sections(preprocessed_nl_sections, lang)
    line_list = get_line_list(nl_sections, orig_file_path)
    preprocessed_nl_line_list = preprocess_nl_line_list(
        nl_sections, line_list, lang)
    line_tuple = beautify_line_list(preprocessed_nl_line_list)
    file_dict = {temp_file_name: line_tuple}
    return file_dict
