def mode_normal(console_printer, log_printer, args, debug=False):
    """
    This is the default coala mode. User interaction is allowed in this mode.

    :param console_printer: Object to print messages on the console.
    :param log_printer:     Deprecated.
    :param args:            Alternative pre-parsed CLI arguments.
    :param debug:           Run in debug mode, bypassing multiprocessing,
                            and not catching any exceptions.
    """
    import functools
    import logging

    from coalib.coala_main import run_coala
    from coalib.output.ConsoleInteraction import (
        acquire_settings, nothing_done,
        print_results, print_section_beginning)

    partial_print_sec_beg = functools.partial(
        print_section_beginning,
        console_printer)
    results, exitcode, _ = run_coala(
        print_results=print_results,
        acquire_settings=acquire_settings,
        print_section_beginning=partial_print_sec_beg,
        nothing_done=nothing_done,
        console_printer=console_printer,
        args=args,
        debug=debug)
    if log_printer:
        logging.warn('log_printer is deprecated. Please do not use it.')

    return exitcode


def mode_non_interactive(console_printer, args, debug=False):
    import functools

    from coalib.coala_main import run_coala
    from coalib.output.ConsoleInteraction import (
        print_results_no_input, print_section_beginning)

    partial_print_sec_beg = functools.partial(
        print_section_beginning,
        console_printer)
    results, exitcode, _ = run_coala(
        print_results=print_results_no_input,
        print_section_beginning=partial_print_sec_beg,
        force_show_patch=True,
        console_printer=console_printer,
        args=args,
        debug=debug)

    return exitcode


def mode_json(args, debug=False):
    import json

    from coalib.coala_main import run_coala
    from coalib.output.Logging import configure_json_logging
    from coalib.output.JSONEncoder import create_json_encoder

    if args.log_json:
        log_stream = configure_json_logging()

    JSONEncoder = create_json_encoder(use_relpath=args.relpath)

    results, exitcode, _ = run_coala(args=args, debug=debug)

    retval = {'results': results}

    if args.log_json:
        retval['logs'] = [json.loads(line) for line in
                          log_stream.getvalue().splitlines()]

    if args.output:
        filename = str(args.output[0])
        with open(filename, 'w') as fp:
            json.dump(retval, fp,
                      cls=JSONEncoder,
                      sort_keys=True,
                      indent=2,
                      separators=(',', ': '))
    else:
        print(json.dumps(retval,
                         cls=JSONEncoder,
                         sort_keys=True,
                         indent=2,
                         separators=(',', ': ')))

    return 0 if args.show_bears else exitcode


def mode_format(args, debug=False):
    from coalib.coala_main import run_coala
    from coalib.output.ConsoleInteraction import print_results_formatted

    _, exitcode, _ = run_coala(
            print_results=print_results_formatted, args=args, debug=debug)
    return exitcode


def mode_converter(args):
    """
    Converts a TOML document into a coafile document
    and vice versa

    :param args: Alternative pre-parsed CLI arguments.
    """
    import os
    from coalib.output.ConfigConverter import ConfigConverter
    from coalib.settings.ConfigurationGathering import (load_config_file,
                                                        load_toml_config_file)
    import sys
    import logging

    input_file = args.config_converter[0]
    output_file = args.config_converter[1]
    _, in_ext = os.path.splitext(input_file)
    if in_ext == '' and _ == '.coafile':
        in_ext = '.coafile'
    _, out_ext = os.path.splitext(output_file)
    if out_ext == '' and _ == '.coafile':
        out_ext = '.coafile'
    converter = ConfigConverter(output_file)

    if in_ext == '.toml' and out_ext == '.coafile':
        sections = load_toml_config_file(input_file)
        converter.toml_to_coafile(sections)
    elif in_ext == '.coafile' and out_ext == '.toml':
        sections = load_config_file(input_file)
        converter.coafile_to_toml(sections)
    else:
        logging.error('Unsupported file formats used. '
                      'The tool can handle conversion between '
                      'coafile and toml formats only')
        sys.exit()
