import os
from argparse import ArgumentParser
from collections import OrderedDict

from coalib.parsing.DefaultArgParser import default_arg_parser
from coalib.parsing.LineParser import LineParser
from coalib.settings.Section import Section, append_to_sections


def parse_cli(arg_list=None,
              origin=os.getcwd(),
              arg_parser=None,
              args=None,
              key_value_delimiters=('=', ':'),
              comment_seperators=(),
              key_delimiters=(',',),
              section_override_delimiters=('.',),
              key_value_append_delimiters=('+=',)):
    """
    Parses the CLI arguments and creates sections out of it.

    :param arg_list:                    The CLI argument list.
    :param origin:                      Directory used to interpret relative
                                        paths given as argument.
    :param arg_parser:                  Instance of ArgParser that is used to
                                        parse none-setting arguments.
    :param args:                        Alternative pre-parsed CLI arguments.
    :param key_value_delimiters:        Delimiters to separate key and value
                                        in setting arguments where settings are
                                        being defined.
    :param comment_seperators:          Allowed prefixes for comments.
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
    assert not (arg_list and args), (
        'Either call parse_cli() with an arg_list of CLI arguments or '
        'with pre-parsed args, but not with both.')

    if args is None:
        arg_parser = default_arg_parser() if arg_parser is None else arg_parser
        args = arg_parser.parse_args(arg_list)

    origin += os.path.sep
    sections = OrderedDict(cli=Section('cli'))
    line_parser = LineParser(key_value_delimiters,
                             comment_seperators,
                             key_delimiters,
                             {},
                             section_override_delimiters,
                             key_value_append_delimiters)

    for arg_key, arg_value in sorted(vars(args).items()):
        if arg_key == 'settings' and arg_value is not None:
            parse_custom_settings(sections,
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
                               section_name='cli',
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
        (_, key_tuples, value, append, _) = line_parser._parse(
            setting_definition)
        for key_tuple in key_tuples:
            append_to_sections(sections,
                               key=key_tuple[1],
                               value=value,
                               origin=origin,
                               to_append=append,
                               section_name=(key_tuple[0] or 'cli'),
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

        if (
                not section.get('json', False) and
                (str(section.get('output', '')) or
                 section.get('relpath', False))):
            ArgumentParser().error(
                "'output' or 'relpath' cannot be used without `--json`.")

    return True
