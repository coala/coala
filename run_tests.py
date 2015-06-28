#!/usr/bin/env python3

import os
import tempfile
from site import getsitepackages

from coalib.tests.TestHelper import (TestHelper,
                                     create_argparser,
                                     run_tests,
                                     get_test_files)


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

    testhelper = TestHelper(parser)

    ignore_list = ([os.path.join(x, "**") for x in getsitepackages()] +
                   [os.path.join(tempfile.gettempdir(), "**")])

    # Project specific ignore list.
    ignore_list += [
        os.path.join("coalib", "tests", "**"),
        os.path.join("coalib", "bearlib", "parsing", "clang", "**"),
        os.path.join("bears", "tests", "**")]

    if not testhelper.args.ignore_main_tests:
        (test_files,
         test_file_names) = get_test_files(
            os.path.abspath(os.path.join("coalib", "tests")),
            test_only=testhelper.args.test_only,
            omit=testhelper.args.omit)
        testhelper.test_files += test_files
        testhelper.test_file_names += test_file_names
    else:
        ignore_list.append(os.path.join("coalib", "**"))

    if not testhelper.args.ignore_bear_tests:
        (test_files,
         test_file_names) = get_test_files(
            os.path.abspath(os.path.join("bears", "tests")),
            test_only=testhelper.args.test_only,
            omit=testhelper.args.omit)
        testhelper.test_files += test_files
        testhelper.test_file_names += test_file_names

    exit(run_tests(ignore_list,
                   testhelper.args,
                   testhelper.test_files,
                   testhelper.test_file_names))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Program terminated by user.")
        exit(130)

    exit(0)
