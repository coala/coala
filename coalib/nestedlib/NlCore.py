from coalib.nestedlib.NlInfoExtractor import generate_arg_list
from coalib.parsing.DefaultArgParser import default_arg_parser
from coalib.nestedlib.NlCliParsing import parse_nl_cli
from collections import OrderedDict
from importlib import import_module

from coalib.parsing.DefaultArgParser import default_arg_parser
import logging
from copy import deepcopy
from coalib.settings.Setting import glob_list
import shutil
from coala_utils.FileUtils import detect_encoding


# The supported Parser for the language combination
PARSER_LANG_COMB = [{'PyJinjaParser': {'python', 'jinja2'}}]


def get_parser(lang_comb):
    """
    Return the parser object for the combination of the languages
    """
    lang_comb = set(lang_comb.split(','))
    parser_name = ''

    for parser_lang_comb in PARSER_LANG_COMB:
        for parser, language in parser_lang_comb.items():
            if language == lang_comb:
                parser_name = parser

    parser_module_string = ('coalib.nestedlib.parsers.' + parser_name)
    try:
        parser = getattr(import_module(parser_module_string), parser_name)
    except ImportError:
        logging.error('No Parser found for the languages combination')
        raise SystemExit(2)

    return parser()


def get_nl_coala_sections(args=None, arg_list=None, arg_parser=None):
    """
    Generate the coala sections for all the nested languages.
    """
    assert not (arg_list and args), (
        'Either call parse_cli() with an arg_list of CLI arguments or '
        'with pre-parsed args, but not with both.')

    if args is None:
        arg_parser = default_arg_parser() if arg_parser is None else arg_parser
        args = arg_parser.parse_args(arg_list)

    arg_list, nl_info_dict = generate_arg_list(args)
    nl_sections = OrderedDict()
    for args in arg_list:
        temp_file_name = args.__dict__['files']
        nl_section_name = 'cli_nl_section: ' + temp_file_name
        sections = parse_nl_cli(args=args,
                                nl_section_name=nl_section_name,
                                nl_info_dict=nl_info_dict)
        nl_sections[nl_section_name] = sections[nl_section_name]

    return nl_sections


def nested_language(args=None, arg_list=None, arg_parser=None):
    """
    Check if handle_nested condition is present in arguments
    """
    handle_nested = False
    # If args is None check if arg_list has handle_nested.
    if args is None:
        arg_parser = default_arg_parser() if arg_parser is None else arg_parser
        nested_args = arg_parser.parse_args(arg_list)
        if nested_args.handle_nested:
            handle_nested = True
    else:
        if args.handle_nested:
            handle_nested = True

    return handle_nested


def get_temp_file_content(nl_file_dicts, temp_file_name):
    """
    Get the temp file dict of temp_file_name from the patched
    nl_file_dicts.

    If you a nested file `test.py` which contains python and jinja as the
    nested language, then the

    nl_file_dicts looks something like this:

    >>> nl_file_dicts =  {
    ...     'cli_nl_section: test.py_nl_python':
    ...         {'test.py_nl_python': ['!!! Start Nl Section: 1\\n',
    ...                                '\\n', '\\n',
    ...                                'def hello():\\n',
    ...                                '\\n', '\\n',
    ...                                '!!! End Nl Section: 1\\n',
    ...                                '\\n', '\\n',
    ...                               ]},
    ...
    ...     'cli_nl_section: test.py_nl_jinja2':
    ...         {'test.py_nl_jinja2': ['\\n',
    ...                                '!!! Start Nl Section: 2\\n',
    ...                                '    {{ x }} asdasd {{ Asd }}\\n',
    ...                                '!!! End Nl Section: 2\\n',
    ...                                ]},
    ... }
    """
    temp_file_content = {}
    for nl_coala_section, temp_file in nl_file_dicts.items():
        for filename, file_content in temp_file.items():
            if temp_file_name == filename:
                temp_file_content = file_content
                break
    return temp_file_content


def remove_position_markers(temp_file_content):
    """
    Remove the position markers from the line.

    Return a dicitionary where the key is the section index and the value
    is the content of the section index.

    We we encounter a `Start Nl Section` string, we extract the index from
    it and keep appending all the lines into a lines_list until we reach the
    `End Nl Section` string of the same index. Then we make a dictionary
    with the key as the section index and the value as the list of lines
    that were present inside the section.

    For eg:

    Input -

    >>> input_list = ['!!! Start Nl Section: 1\\n', '\\n', '\\n',
    ...               'def hello():\\n',
    ...               '!!! End Nl Section: 1\\n', '\\n',
    ...              ]

    The output we receive is:
    >>> output = {1: ['\\n', '\\n', 'def hello():\\n', '\\n']}
    """
    section_index_lines_dict = {}
    section_index = None
    append_lines = False
    line_list = []

    for line in temp_file_content:

        if 'Start Nl Section: ' in line:
            section_index = int(line.split(': ')[1])
            append_lines = True
            continue

        elif 'End Nl Section: ' in line:
            section_index_lines_dict[section_index] = deepcopy(line_list)
            append_lines = False
            section_index = None
            line_list.clear()

        if append_lines:
            line_list.append(line)

    return section_index_lines_dict


def get_linted_file_sections(nl_file_dicts, nl_file_info_dict):
    """
    Generate the linted file dict for every original file.

    This dictionary contains section_index as the key and the content
    in those sections as the value.

    We'll get the file_dict of the temporary files of each original file,
    process the file dict to remove the position markers and then create a
    new file dictionary, where we store the key as the section index and the
    content of that section as it's value.

    Something like:

    >>> linted_file_sections =  {'test.py': {
    ...                                   1:['def hello(): \\n'] ,
    ...                                   2:['\\n', '\\n'],
    ...                                   3:['    {{ x }} asdasd {{ Asd }}\\n'],
    ...                                   4:['{{ x }}\\n']
    ...                         }
    ... }

    nl_info_dict looks something like:
    >>> nl_info_dict = {    'test.py' : {
    ...                                     'python' : 'test.py_nl_python',
    ...                                     'jinja2' : 'test.py_nl_jinja2'
    ...                                 },
    ...
    ...                     'test2.py': {
    ...                                     'python' : 'test2.py_nl_python',
    ...                                     'jinja2' : 'test2.py_nl_jinja2'
    ...                                 }
    ...                }

    """

    file_dicts = {}

    for orig_file, temp_file_info in nl_file_info_dict.items():
        for lang, temp_filename in temp_file_info.items():
            temp_file_content = get_temp_file_content(nl_file_dicts,
                                                      temp_filename)

            # PostProcess the lines to remove the position markers
            # Generate a dict which has the key as the section index
            # and the value as the content of the section. This will
            # help in assembling.
            section_index_lines = remove_position_markers(
                                                    temp_file_content)
            if not file_dicts.get(orig_file):
                file_dicts[orig_file] = section_index_lines
            else:
                file_dicts[orig_file].update(section_index_lines)

    return file_dicts


def generate_linted_file_dict(nl_file_dicts, nl_file_info_dict):
    """
    Generate a dict with the orig_filename as the key and the value as the
    file contents of the file.

    Use the section indexes present in the original_file_dict to assemble
    all the sections and generate the actual linted file.

    Linted file looks like:

    >>> linted_file = { 'test.py': {
    ...                              1:['def hello(): \\n'],
    ...                              2:['\\n', '\\n'],
    ...                              3:['    {{ x }} asdasd {{ Asd }}\\n'],
    ...                              4:['{{ x }}\\n']
    ...                            },
    ...                'test2.py': {
    ...                              1:['print("Hello Homosapiens")'],
    ...                              2:['{% set x = {{var}} %}']
    ...                             }
    ... }


    The sections are sorted according to their index and their content
    are combined to make one list. This list will then be written into a file.

    >>> file_list_to_return = {
    ...                        'test.py':  ['def hello(): \\n',
    ...                                     '\\n',
    ...                                     '\\n',
    ...                                     '    {{ x }} asdasd {{ Asd }}\\n',
    ...                                     '{{ x }}\\n'],
    ...
    ...                        'test2.py': ['print("Hello Homosapiens")',
    ...                                    '{% set x = {{var}} %}']
    ...
    ...
    ...                      }
    """
    linted_file_dict = {}
    linted_file_sections = get_linted_file_sections(
        nl_file_dicts, nl_file_info_dict)
    for file, section_line_dict in linted_file_sections.items():
        # Create an entry for the file, if it's not already present.
        # Useful when we pass multiple files in `--files` argument.
        linted_file_dict[file] = []
        for section_index in sorted(section_line_dict):
            section_content = section_line_dict[section_index]
            linted_file_dict[file].extend(section_content)

    return linted_file_dict


def write_patches_to_orig_nl_file(linted_file_dict, sections):
    """
    Update the original Nested language file with the patches that the user
    chose to apply.

    We create a backup with the extension of `.orig` similar to how coala
    does when it writes the patches to the file.
    """
    for filename, patched_filecontent in linted_file_dict.items():
        orig_file_path = get_original_file_path(sections, filename)
        # Backup original file
        shutil.copy2(orig_file_path, orig_file_path + '.orig')

        with open(orig_file_path, mode='w',
                  encoding=detect_encoding(orig_file_path)) as file:
            file.writelines(patched_filecontent)

    return


def get_original_file_path(sections, filename):
    """
    Return the path where the file is located.
    """
    file_path = ''
    for section_name in sections:
        section = sections[section_name]
        if str(section.get('orig_file_name')) == filename:
            file_path = glob_list(section.get('orig_file_name', ''))[0]
            break
    return file_path


def apply_patches_to_nl_file(nl_file_dicts, sections, args=None,
                             arg_list=None, nl_info_dict=None,
                             arg_parser=None):
    """
    :param nl_file_dicts: The linted nested language file dict.
    :param sections:      The coala nl sections.
    :param args:          The args passed in via CLI.
    :parma arg_list:      The arg_list that contains precompiled args
    :param nl_info_dict:  The dicitionary which contains the info of
                          the original file name as the key and the
                          value as the information about the temporary
                          file and the language.

    Write the accepted patches into the original nested language file.

    We assemble the applied patches from all the temporary linted pure
    language file and preprocess it to remove the `nl section position`
    markers and then write it to the original file.

    We can use the generate_arg_list function to get more information about
    the original file and temporary file.
    """

    if args is None:
        arg_parser = default_arg_parser() if arg_parser is None else arg_parser
        args = arg_parser.parse_args(arg_list)

    if not nl_info_dict:
        arg_list, nl_info_dict = generate_arg_list(args)
    nl_file_info_dict = nl_info_dict['nl_file_info']

    linted_file_dict = generate_linted_file_dict(nl_file_dicts,
                                                 nl_file_info_dict)
    write_patches_to_orig_nl_file(linted_file_dict, sections)

    return linted_file_dict
