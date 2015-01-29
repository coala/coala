#!/usr/bin/env python3

import os
import sys
import argparse
import tempfile
from distutils.sysconfig import get_python_lib

from coalib.tests.TestHelper import TestHelper


def show_help():
    print("Usage: {name} [OPTIONS]".format(name=sys.argv[0]))
    print()
    print("--help  : Show this help text")
    print("--cover : Use coverage to get statement and branch coverage of tests")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Executes all tests for coala.",
                                     epilog="Please note that the tests for coala are split into tests for the main "
                                            "program and the bears. By default all these tests are executed, however "
                                            "you can switch them off individually.")
    parser.add_argument("-c", "--cover", help="measure code coverage", action="store_true")
    parser.add_argument("-b", "--ignore-bear-tests", help="ignore bear tests", action="store_true")
    parser.add_argument("-m", "--ignore-main-tests", help="ignore main program tests", action="store_true")
    parser.add_argument("-v", "--verbose", help="more verbose output", action="store_true")
    parser.add_argument("-o", "--omit", help="base names of tests to omit", nargs="+")
    args = parser.parse_args()

    omit = args.omit
    if omit is None:
        omit = []

    files = []
    if not args.ignore_main_tests:
        files.extend(TestHelper.get_test_files(os.path.abspath("coalib/tests"), omit))
    if not args.ignore_bear_tests:
        files.extend(TestHelper.get_test_files(os.path.abspath("bears/tests"), omit))

    ignore_list = files[:]
    ignore_list.extend([
        os.path.join(tempfile.gettempdir(), "*"),
        os.path.join(get_python_lib(), "*")
    ])

    exit(TestHelper.execute_python3_files(files, args.cover, ignore_list, args.verbose))
