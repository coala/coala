import argparse
import importlib
import inspect
import os
import subprocess
import sys
import shutil
import webbrowser
from coalib.misc.ContextManagers import (suppress_stdout,
                                         preserve_sys_path,
                                         subprocess_timeout)
from coalib.misc.StringConstants import StringConstants
from coalib.processes.Processing import create_process_group


def create_argparser(**kwargs):
    parser = argparse.ArgumentParser(**kwargs)
    parser.add_argument("-t",
                        "--test-only",
                        help="Execute only the tests with the "
                             "given base name",
                        nargs="+")
    parser.add_argument("-c",
                        "--cover",
                        help="Measure code coverage",
                        action="store_true")
    parser.add_argument("-H",
                        "--html",
                        help="Generate html code coverage, implies -c",
                        action="store_true")
    parser.add_argument("-v",
                        "--verbose",
                        help="More verbose output",
                        action="store_true")
    parser.add_argument("-o",
                        "--omit",
                        help="Base names of tests to omit",
                        nargs="+")
    parser.add_argument("-s",
                        "--disallow-test-skipping",
                        help="Return nonzero if any tests are skipped "
                             "or fail",
                        action="store_true")
    parser.add_argument("-T",
                        "--timeout",
                        default=10,
                        type=int,
                        help="Amount of time to wait for a test to run "
                             "before killing it. To not use any timeout, "
                             "set this to 0")

    return parser


def parse_args(parser):
    """
    Parses the CLI arguments.

    :param parser: A argparse.ArgumentParser created with the
                   create_argparser method of TestHelper module.
    :return args:  The parsed arguments.
    """
    args = parser.parse_args()
    args = resolve_implicit_args(args, parser)

    return args


def resolve_implicit_args(args, parser):
    args.cover = args.cover or args.html
    if args.omit is not None and args.test_only is not None:
        parser.error("Incompatible options: --omit and --test_only")
    if args.omit is None:
        args.omit = []
    if args.test_only is None:
        args.test_only = []

    return args


def is_eligible_test(filename, test_only, omit):
    """
    Checks if the filename is a Test or not. The conditions are:
     - Ends with "Test.py"
     - Is not present in `omit`
     - If test_only is not empty, it should be present in test_only

    :param filename:  The filename to check eligibility for.
    :param test_only: Only execute files within the filenames in this list.
    :param omit:      The filename should not be in this list.
    return:           True if the file is eligible to be run as a test,
                      else False.
    """
    if not filename.endswith("Test.py"):
        return False
    name = os.path.splitext(os.path.basename(filename))[0]
    if name in omit:
        return False
    if (len(test_only) > 0) and (name not in test_only):
        return False

    return True


def delete_coverage():
    """
    Deletes previous coverage data.

    :return: False if coverage3 cannot be executed.
    """
    coverage_available = False
    with suppress_stdout():
        coverage_available = subprocess.call(
            [StringConstants.python_executable,
             "-m",
             "coverage",
             "erase"]) == 0
    if not coverage_available:
        print("Coverage failed. Falling back to standard unit tests."
              "Install code coverage measurement for python3. Package"
              "name should be something like: python-coverage3/coverage")

    return coverage_available


def execute_command_array(command_array, timeout, verbose):
    timed_out = False

    p = create_process_group(command_array,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             universal_newlines=True)
    with subprocess_timeout(p,
                            timeout,
                            kill_pg=True) as timedout:
        retval = p.wait()
        timed_out = timedout.value

    if retval != 0 or verbose:
        for line in p.stderr:
            print(line, end='')
        for line in p.stdout:
            print(line, end='')

    if timed_out:
        print("This test failed because it was taking more than", timeout,
              "sec to execute. To change the timeout setting use the `-T` or "
              "`--timeout` argument.")

    return retval


def check_module_skip(filename):
    with preserve_sys_path(), suppress_stdout():
        module_dir = os.path.dirname(filename)
        if module_dir not in sys.path:
            sys.path.insert(0, module_dir)

        try:
            module = importlib.import_module(
                os.path.basename(os.path.splitext(filename)[0]))

            for name, obj in inspect.getmembers(module):
                if inspect.isfunction(obj) and name == "skip_test":
                    return obj()
        except ImportError as exception:
            return str(exception)

        return False


def show_coverage_results(html):
    subprocess.call([StringConstants.python_executable,
                     "-m",
                     "coverage",
                     "combine"])
    subprocess.call([StringConstants.python_executable,
                     "-m",
                     "coverage",
                     "report",
                     "-m"])
    if html:
        shutil.rmtree(".htmlreport", ignore_errors=True)
        print("Generating HTML report to .htmlreport...")
        subprocess.call([StringConstants.python_executable,
                         "-m",
                         "coverage",
                         "html",
                         "-d",
                         ".htmlreport"])
        try:
            webbrowser.open_new_tab(os.path.join(".htmlreport",
                                                 "index.html"))
        except webbrowser.Error:
            pass


def execute_python_file(filename, ignored_files, cover, timeout, verbose):
    if not cover:
        return execute_command_array([StringConstants.python_executable,
                                      filename],
                                     timeout=timeout,
                                     verbose=verbose)

    return execute_command_array([StringConstants.python_executable,
                                  "-m",
                                  "coverage",
                                  "run",
                                  "-p",  # make it collectable later
                                  "--branch",
                                  "--omit",
                                  ignored_files,
                                  filename],
                                 timeout=timeout,
                                 verbose=verbose)


def show_nonexistent_tests(test_only, test_file_names):
    nonexistent_tests = 0
    number = len(test_only)
    for test in test_only:
        if test not in test_file_names:
            nonexistent_tests += 1
            print(" {:>2}/{:<2} | {}, Cannot execute: This test does "
                  "not exist.".format(nonexistent_tests, number, test))

    return nonexistent_tests, number


def execute_test(filename,
                 curr_nr,
                 max_nr,
                 ignored_files,
                 verbose,
                 cover,
                 timeout):
    """
    Executes the given test and counts up failed_tests or skipped_tests if
    needed.

    :param filename:      Filename of test to execute.
    :param curr_nr:       Number of current test.
    :param max_nr:        Count of all tests.
    :param ignored_files: Comma separated list of files to ignore for coverage.
    :param verbose:       Boolean to show more information.
    :param cover:         Boolean to calculate coverage information or not.
    :param timeout:       Time in seconds to wait for the test to complete
                          before killing it. Floats are allowed for units
                          smaller than a second.
    :return:              Returns a tuple with (failed_tests, skipped_tests).
                          As this executes one file, the tuple will be either
                          (0, 0) or (0, 1) or (1, 0).
    """
    basename = os.path.splitext(os.path.basename(filename))[0]
    reason = check_module_skip(filename)
    if reason is not False:
        print(" {:>2}/{:<2} | {}, Skipping: {}".format(curr_nr,
                                                       max_nr,
                                                       basename,
                                                       reason))
        return 0, 1
    else:
        print(" {:>2}/{:<2} | {}".format(curr_nr, max_nr, basename))
        result = execute_python_file(filename,
                                     ignored_files,
                                     cover=cover,
                                     timeout=timeout,
                                     verbose=verbose)
        if verbose or result != 0:
            print("#" * 70)

        return result, 0


def get_test_files(testdir, test_only, omit):
    """
    Searches within a directory for all files which could contain tests. Uses
    the `is_eligible_test` function internally to get a list of files.

    :param testdir:   The directory to search in.
    :param test_only: Only accepts tests within the filenames in this list.
    :param omit:      Does not use filenames in this list.
    :return:          A tuple containing a list of file paths which need to be
                      executed and a list of the name of the file (without the
                      extension).

    """
    test_files = []
    test_file_names = []
    for (dirpath, dirnames, filenames) in os.walk(testdir):
        for filename in filenames:
            if is_eligible_test(filename,
                                test_only=test_only,
                                omit=omit):
                test_files.append(os.path.join(dirpath, filename))
                test_file_names.append(
                    os.path.splitext(os.path.basename(filename))[0])
    return test_files, test_file_names


def run_tests(ignore_list, args, test_files, test_file_names):
    failed_tests = 0
    skipped_tests = 0
    if args.cover:
        args.cover = delete_coverage()

    if len(args.test_only) > 0:
        (nonexistent_tests,
         number) = show_nonexistent_tests(args.test_only,
                                          test_file_names)
        failed_tests += nonexistent_tests
    else:
        number = len(test_files)
        nonexistent_tests = 0

    # Sort tests alphabetically.
    test_files.sort(key=lambda fl: str.lower(os.path.split(fl)[1]))

    for i, file in enumerate(test_files):
        _failed_tests, _skipped_tests = execute_test(
            file,
            i+nonexistent_tests+1,
            number,
            ",".join(ignore_list),
            verbose=args.verbose,
            cover=args.cover,
            timeout=args.timeout)
        failed_tests += _failed_tests
        skipped_tests += _skipped_tests

    print("\nTests finished: failures in {} of {} test modules, skipped "
          "{} test modules.".format(failed_tests,
                                    number,
                                    skipped_tests))

    if args.cover:
        show_coverage_results(args.html)

    if not args.disallow_test_skipping:
        return failed_tests
    else:
        return failed_tests + skipped_tests
