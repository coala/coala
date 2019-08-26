import os
from argparse import ArgumentParser
from collections import OrderedDict
from coalib.nestedlib.NlInfoExtractor import (
    get_orig_file, get_temp_file_lang)
from coalib.parsing.LineParser import LineParser
from coalib.settings.Section import Section, append_to_sections
from coalib.bearlib import deprecate_settings


@deprecate_settings(comment_separators='comment_seperators')
def parse_nl_cli(args=None,
                 nl_section_name=None,
                 nl_info_dict=None,
                 origin=os.getcwd(),
                 key_value_delimiters=('=', ':'),
                 comment_separators=(),
                 key_delimiters=(',',),
                 section_override_delimiters=('.',),
                 key_value_append_delimiters=('+=',)):
    """
    Parses the CLI arguments and creates sections out of it.

    :param origin:                      Directory used to interpret relative
                                        paths given as argument.
    :param args:                        Alternative pre-parsed CLI arguments.
    :param key_value_delimiters:        Delimiters to separate key and value
                                        in setting arguments where settings are
                                        being defined.
    :param comment_separators:          Allowed prefixes for comments.
    :param key_delimiters:              Delimiter to separate multiple keys of
                                        a setting argument.
    :param section_override_delimiters: The delimiter to delimit the section
                                        from the key name (e.g. the '.' in
                                        sect.key = value).
    :param key_value_append_delimiters: Delimiters to separate key and value
                                        in setting arguments where settings are
                                        being appended.
    :return:                            A dictionary holding section names
                                        as keys and the sections themselves
                                        as value.
    """

    origin += os.path.sep
    sections = OrderedDict()
    sections[nl_section_name] = Section(nl_section_name)
    line_parser = LineParser(key_value_delimiters,
                             comment_separators,
                             key_delimiters,
                             {},
                             section_override_delimiters,
                             key_value_append_delimiters)

    for arg_key, arg_value in sorted(vars(args).items()):
        if arg_key == 'settings' and arg_value is not None:
            parse_nl_custom_settings(sections,
                                     nl_section_name,
                                     arg_value,
                                     origin,
                                     line_parser)
        else:
            if isinstance(arg_value, list):
                arg_value = ','.join([str(val) for val in arg_value])

            append_to_sections(sections,
                               arg_key,
                               arg_value,
                               origin,
                               section_name=nl_section_name,
                               from_cli=True)

    temp_file_name = args.__dict__['files']
    # The following values are necessary to help detect the parser and for
    # reassembling.
    # Append the language of the temporary segregated file
    append_to_sections(sections,
                       'file_lang',
                       get_temp_file_lang(nl_info_dict, temp_file_name),
                       origin=origin,
                       section_name=nl_section_name,
                       from_cli=True)

    # Append the name of the original nested file
    append_to_sections(sections,
                       'orig_file_name',
                       get_orig_file(nl_info_dict, temp_file_name),
                       origin=origin,
                       section_name=nl_section_name,
                       from_cli=True)

    return sections


def parse_nl_custom_settings(sections,
                             nl_section_name,
                             custom_settings_list,
                             origin,
                             line_parser):
    """
    Parses the custom settings given to coala via ``-S something=value``.

    :param sections:             The Section dictionary to add to (mutable).
    :param nl_section_name:      The name of the nested language coala section
    :param custom_settings_list: The list of settings strings.
    :param origin:               The originating directory.
    :param line_parser:          The LineParser to use.
    """
    for setting_definition in custom_settings_list:
        (_, key_tuples, value, append, _) = line_parser._parse(
            setting_definition)
        for key_tuple in key_tuples:
            append_to_sections(sections,
                               key=key_tuple[1],
                               value=value,
                               origin=origin,
                               to_append=append,
                               section_name=(key_tuple[0] or nl_section_name),
                               from_cli=True)


def check_conflicts(sections):
    """
    Checks if there are any conflicting arguments passed.

    :param sections:    The ``{section_name: section_object}`` dictionary to
                        check conflicts for.
    :return:            True if no conflicts occur.
    :raises SystemExit: If there are conflicting arguments (exit code: 2)
    """
    for section in sections.values():
        if (
                section.get('no_config', False) and
                (section.get('save', False) or
                 section.get('find_config', False) or
                 str(section.get('config', 'input')) != 'input')):
            ArgumentParser().error(
                "'no_config' cannot be set together with 'save', "
                "'find_config' or 'config'.")

        if (
                not section.get('json', False) and
                (str(section.get('output', '')) or
                 section.get('relpath', False))):
            ArgumentParser().error(
                "'output' or 'relpath' cannot be used without `--json`.")

    return True
