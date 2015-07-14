#!/usr/bin/env python3

import os
import tempfile
from site import getsitepackages

from coalib.misc import i18n
from coalib import assert_supported_version

assert_supported_version()

from coalib.tests.TestUtilities import (parse_args,
                                        create_argparser,
                                        run_tests,
                                        get_test_files,
                                        delete_coverage)


def main():
    parser = create_argparser(description="Runs coalas tests.")
    parser.add_argument("-b",
                        "--ignore-bear-tests",
                        help="ignore bear tests",
                        action="store_true")
    parser.add_argument("-m",
                        "--ignore-main-tests",
                        help="ignore main program tests",
                        action="store_true")

    args = parse_args(parser)
    test_files = []
    test_file_names = []

    ignore_list = ([os.path.join(x, "**") for x in getsitepackages()] +
                   [os.path.join(tempfile.gettempdir(), "**")])

    # Project specific ignore list.
    ignore_list += [
        os.path.join("coalib", "tests", "**"),
        os.path.join("coalib", "bearlib", "parsing", "clang", "**"),
        os.path.join("bears", "tests", "**")]

    if not args.ignore_main_tests:
        (main_test_files,
         main_test_file_names) = get_test_files(
            os.path.abspath(os.path.join("coalib", "tests")),
            test_only=args.test_only,
            omit=args.omit)
        test_files += main_test_files
        test_file_names += main_test_file_names
    else:
        ignore_list.append(os.path.join("coalib", "**"))

    if not args.ignore_bear_tests:
        (bear_test_files,
         bear_test_file_names) = get_test_files(
            os.path.abspath(os.path.join("bears", "tests")),
            test_only=args.test_only,
            omit=args.omit)
        test_files += bear_test_files
        test_file_names += bear_test_file_names

    # Compile translations
    i18n.compile_translations()

    exit(run_tests(ignore_list,
                   args,
                   test_files,
                   test_file_names))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Program terminated by user.")
        print("Cleaning up...")
        delete_coverage(silent=True)
        print("Done!")
        exit(130)

    exit(0)
