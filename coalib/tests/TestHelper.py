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


class TestHelper:
    @staticmethod
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

    def __init__(self, parser):
        """
        Creates a new test helper and with it parses the CLI arguments.

        :param parser: A argparse.ArgumentParser created with the
                       create_argparser method of this class.
        """
        self.parser = parser
        self.args = self.parser.parse_args()
        self.__resolve_implicit_args()
        self.test_files = []
        self.test_file_names = []
        self.failed_tests = 0
        self.skipped_tests = 0

    def delete_coverage(self):
        """
        Deletes previous coverage data and adjusts the args.cover member to
        False if coverage3 is unavailable.

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
            self.args.cover = False  # Don't use coverage if this fails
        return coverage_available

    def run_tests(self, ignore_list):
        if self.args.cover:
            self.delete_coverage()

        if len(self.args.test_only) > 0:
            nonexistent_tests, number = self.show_nonexistent_tests()
        else:
            number = len(self.test_files)
            nonexistent_tests = 0

        # Sort tests alphabetically.
        self.test_files.sort(key=lambda fl: str.lower(os.path.split(fl)[1]))

        for i, file in enumerate(self.test_files):
            self.__execute_test(file,
                                i+nonexistent_tests+1,
                                number,
                                ",".join(ignore_list))

        print("\nTests finished: failures in {} of {} test modules, skipped "
              "{} test modules.".format(self.failed_tests,
                                        number,
                                        self.skipped_tests))

        if self.args.cover:
            self.__show_coverage_results()

        if not self.args.disallow_test_skipping:
            return self.failed_tests
        else:
            return self.failed_tests + self.skipped_tests

    def show_nonexistent_tests(self):
        nonexistent_tests = 0
        number = len(self.args.test_only)
        for test in self.args.test_only:
            if test not in self.test_file_names:
                nonexistent_tests += 1
                self.failed_tests += 1
                print(" {:>2}/{:<2} | {}, Cannot execute: This test does "
                      "not exist.".format(nonexistent_tests, number, test))

        return nonexistent_tests, number

    def add_test_files(self, testdir):
        for (dirpath, dirnames, filenames) in os.walk(testdir):
            for filename in filenames:
                if self.__is_eligible_test(filename):
                    self.test_files.append(os.path.join(dirpath, filename))
                    self.test_file_names.append(
                        os.path.splitext(os.path.basename(filename))[0])

    def __resolve_implicit_args(self):
        self.args.cover = self.args.cover or self.args.html
        if self.args.omit is not None and self.args.test_only is not None:
            self.parser.error("Incompatible options: --omit and --test_only")
        if self.args.omit is None:
            self.args.omit = []
        if self.args.test_only is None:
            self.args.test_only = []

    def __show_coverage_results(self):
        subprocess.call([StringConstants.python_executable,
                         "-m",
                         "coverage",
                         "combine"])
        subprocess.call([StringConstants.python_executable,
                         "-m",
                         "coverage",
                         "report",
                         "-m"])
        if self.args.html:
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

    def __print_output(self, command_array):
        timed_out = False

        p = create_process_group(command_array,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 universal_newlines=True)
        with subprocess_timeout(p,
                                self.args.timeout,
                                kill_pg=True) as timedout:
            retval = p.wait()
            timed_out = timedout.value

        if retval != 0 or self.args.verbose:
            for line in p.stderr:
                print(line, end='')
            for line in p.stdout:
                print(line, end='')

        if timed_out:
            print("This test failed because it was taking more than",
                  self.args.timeout, "sec to execute. To change the "
                  "timeout setting use the `-T` or `--timeout` argument.")

        return retval

    def __execute_python3_file(self, filename, ignored_files):
        if not self.args.cover:
            return self.__print_output([StringConstants.python_executable,
                                        filename])

        return self.__print_output([StringConstants.python_executable,
                                    "-m",
                                    "coverage",
                                    "run",
                                    "-p",  # make it collectable later
                                    "--branch",
                                    "--omit",
                                    ignored_files,
                                    filename])

    @staticmethod
    def __check_module_skip(filename):
        with preserve_sys_path(), suppress_stdout():
            module_dir = os.path.dirname(filename)
            if module_dir not in sys.path:
                sys.path.insert(0, module_dir)

            try:
                module = importlib.import_module(
                    os.path.basename(os.path.splitext(filename)[0]))

                for name, object in inspect.getmembers(module):
                    if inspect.isfunction(object) and name == "skip_test":
                        return object()
            except ImportError as exception:
                return str(exception)

            return False

    def __execute_test(self, filename, curr_nr, max_nr, ignored_files):
        """
        Executes the given test and counts up failed_tests or skipped_tests if
        needed.

        :param filename:      Filename of test to execute
        :param curr_nr:       Number of current test
        :param max_nr:        Count of all tests
        :param ignored_files: Files to ignore for coverage
        """
        basename = os.path.splitext(os.path.basename(filename))[0]
        reason = self.__check_module_skip(filename)
        if reason is not False:
            print(" {:>2}/{:<2} | {}, Skipping: {}".format(curr_nr,
                                                           max_nr,
                                                           basename,
                                                           reason))
            self.skipped_tests += 1
        else:
            print(" {:>2}/{:<2} | {}".format(curr_nr, max_nr, basename))
            result = self.__execute_python3_file(filename, ignored_files)
            if self.args.verbose or result != 0:
                print("#" * 70)

            self.failed_tests += result

    def __is_eligible_test(self, filename):
        if not filename.endswith("Test.py"):
            return False
        name = os.path.splitext(os.path.basename(filename))[0]
        if name in self.args.omit:
            return False
        if (
                (len(self.args.test_only) > 0) and
                (name not in self.args.test_only)):
            return False

        return True
