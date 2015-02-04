#!/usr/bin/env python3

import os
import sys
import tempfile
from distutils.sysconfig import get_python_lib

from coalib.tests.TestHelper import TestHelper


def show_help():
    print("Usage: {name} [OPTIONS]".format(name=sys.argv[0]))
    print()
    print("--help  : Show this help text")
    print("--cover : Use coverage to get statement and branch coverage of tests")


if __name__ == '__main__':
    parser = TestHelper.create_argparser(description="Executes all tests for coala.")
    parser.add_argument("-b", "--ignore-bear-tests", help="ignore bear tests", action="store_true")
    parser.add_argument("-m", "--ignore-main-tests", help="ignore main program tests", action="store_true")

    testhelper = TestHelper(parser)

    if not testhelper.args.ignore_main_tests:
        testhelper.add_test_files(os.path.abspath(os.path.join("coalib", "tests")))
    if not testhelper.args.ignore_bear_tests:
        testhelper.add_test_files(os.path.abspath(os.path.join("bears", "tests")))

    ignore_list = [
        os.path.join(tempfile.gettempdir(), "**"),
        os.path.join(get_python_lib(), "**"),
        os.path.join("coalib", "tests", "**"),
        os.path.join("bears", "tests", "**")
    ]

    exit(testhelper.execute_python3_files(ignore_list))
