def mode_normal(console_printer, log_printer):
    import functools

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
        console_printer=console_printer)

    return exitcode


def mode_non_interactive(console_printer, args):
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
        console_printer=console_printer)

    return exitcode


def mode_json(args):
    import json

    from coalib.coala_main import run_coala
    from coalib.misc.DictUtilities import inverse_dicts
    from coalib.misc.Exceptions import get_exitcode
    from coalib.output.Logging import configure_json_logging
    from coalib.output.JSONEncoder import create_json_encoder
    from coalib.output.printers.LogPrinter import LogPrinter
    from coalib.settings.ConfigurationGathering import get_filtered_bears

    if args.log_json:
        log_stream = configure_json_logging()

    JSONEncoder = create_json_encoder(use_relpath=args.relpath)
    results = []

    if args.show_bears:
        try:
            local_bears, global_bears = get_filtered_bears(
                args.filter_by_language, LogPrinter())
            bears = inverse_dicts(local_bears, global_bears)
            for bear, _ in sorted(bears.items(),
                                  key=lambda bear_tuple:
                                  bear_tuple[0].name):
                results.append(bear)
        except BaseException as exception:  # pylint: disable=broad-except
            return get_exitcode(exception)
    else:
        results, exitcode, _ = run_coala()

    retval = {'bears': results} if args.show_bears else {'results': results}

    if args.log_json:
        retval['logs'] = [json.loads(line) for line in
                          log_stream.getvalue().splitlines()]

    if args.output:
        filename = str(args.output[0])
        with open(filename, 'w+') as fp:
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


def mode_format():
    from coalib.coala_main import run_coala
    from coalib.output.ConsoleInteraction import print_results_formatted

    _, exitcode, _ = run_coala(
            print_results=print_results_formatted)
    return exitcode
