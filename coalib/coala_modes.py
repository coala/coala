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


def mode_diff(args, debug=False):
    import json

    from coalib.coala_main import run_coala
    from coalib.output.JSONEncoder import create_json_encoder

    JSONEncoder = create_json_encoder(use_relpath=args.relpath)

    results, exitcode, _ = run_coala(args=args, debug=debug)
    retval = {'results': results}

    # json_data is the output of `--json`
    json_data = json.dumps(retval,
                           cls=JSONEncoder,
                           sort_keys=True,
                           indent=2,
                           separators=(',', ': '))

    # Converting back to dict and discarding all the non-fix results
    data = json.loads(json_data)
    sections = data['results']
    unified_diff = ''
    for _, section_value in sections.items():
        for section_list in section_value:
            for key, val in section_list.items():
                if key == 'diffs' and val is not None:
                    for filename, diff in val.items():
                        diff = diff.replace('+++', '+++ ' + filename)
                        diff = diff.replace('---', '--- ' + filename)
                        unified_diff += diff + '\n'

    # Check if user has used `--output` to mention the output file
    if args.output:
        filename = str(args.output[0])
        with open(filename, 'w') as fp:
            fp.write(unified_diff)
    else:
        print(unified_diff)

    return exitcode


def mode_format(args, debug=False):
    from coalib.coala_main import run_coala
    from coalib.output.ConsoleInteraction import print_results_formatted

    _, exitcode, _ = run_coala(
            print_results=print_results_formatted, args=args, debug=debug)
    return exitcode
