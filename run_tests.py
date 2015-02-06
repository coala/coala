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

    if not testhelper.args.ignore_main_tests:
        testhelper.add_test_files(os.path.abspath(os.path.join("coalib",
                                                               "tests")))
    if not testhelper.args.ignore_bear_tests:
        testhelper.add_test_files(os.path.abspath(os.path.join("bears",
                                                               "tests")))

    print("\033[31;1m", get_python_lib(), "\033[0m")
    ignore_list = [
        os.path.join(tempfile.gettempdir(), "**"),
        os.path.join(os.path.split(tempfile.gettempdir())[0], "**"),
        os.path.join(get_python_lib(), "**"),
        os.path.join("coalib", "tests", "**"),
        os.path.join("bears", "tests", "**")
    ]

    exit(testhelper.execute_python3_files(ignore_list))
