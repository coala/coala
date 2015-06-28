#!/usr/bin/env python3

import os
import tempfile
from site import getsitepackages

from coalib.tests.TestHelper import TestHelper, create_argparser, run_tests


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
        testhelper.add_test_files(os.path.abspath(os.path.join("coalib",
                                                               "tests")))
    else:
        ignore_list.append(os.path.join("coalib", "**"))

    if not testhelper.args.ignore_bear_tests:
        testhelper.add_test_files(os.path.abspath(os.path.join("bears",
                                                               "tests")))

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
