#!/usr/bin/env python3

import os
import tempfile
from distutils.sysconfig import get_python_lib

from coalib.tests.TestHelper import TestHelper


if __name__ == '__main__':
    parser = TestHelper.create_argparser(description="Runs coalas tests.")
    parser.add_argument("-b",
                        "--ignore-bear-tests",
                        help="ignore bear tests",
                        action="store_true")
    parser.add_argument("-m",
                        "--ignore-main-tests",
                        help="ignore main program tests",
                        action="store_true")

    testhelper = TestHelper(parser)

    ignore_list = [
        os.path.join(tempfile.gettempdir(), "**"),
        os.path.join(os.path.dirname(get_python_lib()), "**"),
        os.path.join("coalib", "tests", "**"),
        os.path.join("coalib", "bearlib", "parsing", "clang", "**"),
        os.path.join("bears", "tests", "**")
    ]

    if not testhelper.args.ignore_main_tests:
        testhelper.add_test_files(os.path.abspath(os.path.join("coalib",
                                                               "tests")))
    else:
        ignore_list.append(os.path.join("coalib", "**"))

    if not testhelper.args.ignore_bear_tests:
        testhelper.add_test_files(os.path.abspath(os.path.join("bears",
                                                               "tests")))

    exit(testhelper.run_tests(ignore_list))
