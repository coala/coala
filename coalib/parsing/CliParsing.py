import os
from argparse import ArgumentParser
from collections import OrderedDict

from coalib.parsing.DefaultArgParser import default_arg_parser
from coalib.parsing.LineParser import LineParser
from coalib.settings.Section import Section, append_to_sections


def parse_cli(arg_list=None,
              origin=os.getcwd(),
              arg_parser=None,
              key_value_delimiters=('=', ':'),
              comment_seperators=(),
              key_delimiters=(',',),
              section_override_delimiters=(".",)):
    """
    Parses the CLI arguments and creates sections out of it.

    :param arg_list:                    The CLI argument list.
    :param origin:                      Directory used to interpret relative
                                        paths given as argument.
    :param arg_parser:                  Instance of ArgParser that is used to
                                        parse none-setting arguments.
    :param key_value_delimiters:        Delimiters to separate key and value
                                        in setting arguments.
    :param comment_seperators:          Allowed prefixes for comments.
    :param key_delimiters:              Delimiter to separate multiple keys of
                                        a setting argument.
    :param section_override_delimiters: The delimiter to delimit the section
                                        from the key name (e.g. the '.' in
                                        sect.key = value).
    :return:                            A dictionary holding section names
                                        as keys and the sections themselves
                                        as value.
    """
    arg_parser = default_arg_parser() if arg_parser is None else arg_parser
    origin += os.path.sep
    sections = OrderedDict(default=Section('Default'))
    line_parser = LineParser(key_value_delimiters,
                             comment_seperators,
                             key_delimiters,
                             {},
                             section_override_delimiters)

    for arg_key, arg_value in sorted(
            vars(arg_parser.parse_args(arg_list)).items()):
        if arg_key == 'settings' and arg_value is not None:
            parse_custom_settings(sections,
                                  arg_value,
                                  origin,
                                  line_parser)
        else:
            if isinstance(arg_value, list):
                arg_value = ",".join([str(val) for val in arg_value])

            append_to_sections(sections,
                               arg_key,
                               arg_value,
                               origin,
                               from_cli=True)

    return sections


def parse_custom_settings(sections,
                          custom_settings_list,
                          origin,
                          line_parser):
    """
    Parses the custom settings given to coala via ``-S something=value``.

    :param sections:             The Section dictionary to add to (mutable).
    :param custom_settings_list: The list of settings strings.
    :param origin:               The originating directory.
    :param line_parser:          The LineParser to use.
    """
    for setting_definition in custom_settings_list:
        (_, key_tuples, value, _) = line_parser.parse(setting_definition)
        for key_tuple in key_tuples:
            append_to_sections(sections,
                               key=key_tuple[1],
                               value=value,
                               origin=origin,
                               section_name=key_tuple[0],
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
                 section.get('find_config', False))):
            ArgumentParser().error(
                "'no_config' cannot be set together 'save' or 'find_config'.")

    return True
