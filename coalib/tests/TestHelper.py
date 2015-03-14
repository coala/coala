import argparse
import importlib
import inspect
import os
import subprocess
import sys
import shutil
import webbrowser
import builtins
from coalib.misc.ContextManagers import suppress_stdout


class TestHelper:
    @staticmethod
    def create_argparser(**kwargs):
        parser = argparse.ArgumentParser(**kwargs)
        parser.add_argument("-t",
                            "--test-only",
                            help="execute only the tests with the "
                                 "given base name",
                            nargs="+")
        parser.add_argument("-c",
                            "--cover",
                            help="measure code coverage",
                            action="store_true")
        parser.add_argument("-H",
                            "--html",
                            help="generate html code coverage, implies -c",
                            action="store_true")
        parser.add_argument("-v",
                            "--verbose",
                            help="more verbose output",
                            action="store_true")
        parser.add_argument("-o",
                            "--omit",
                            help="base names of tests to omit",
                            nargs="+")
        parser.add_argument("-s",
                            "--disallow-test-skipping",
                            help="return nonzero if any tests are skipped "
                                 "or fail",
                            action="store_true")

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
        self.failed_tests = 0
        self.skipped_tests = 0

    def delete_coverage(self):
        """
        Deletes previous coverage data and adjusts the args.cover member to
        False if coverage3 is unavailable.

        :return: False if coverage3 cannot be executed.
        """
        try:
            subprocess.call(["coverage3", "erase"])
            return True
        except:
            print("Coverage failed. Falling back to standard unit tests.")
            self.args.cover = False  # Don't use coverage if this fails
            return False

    def run_tests(self, ignore_list):
        if self.args.cover:
            self.delete_coverage()

        number = len(self.test_files)
        for i, file in enumerate(self.test_files):
            self.__execute_test(file, i+1, number, ",".join(ignore_list))

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

    def add_test_files(self, testdir):
        for (dirpath, dirnames, filenames) in os.walk(testdir):
            for filename in filenames:
                if self.__is_eligible_test(filename):
                    self.test_files.append(os.path.join(dirpath, filename))

    def __resolve_implicit_args(self):
        self.args.cover = self.args.cover or self.args.html
        if self.args.omit is not None and self.args.test_only is not None:
            self.parser.error("Incompatible options: --omit and --test_only")
        if self.args.omit is None:
            self.args.omit = []
        if self.args.test_only is None:
            self.args.test_only = []

    def __show_coverage_results(self):
        subprocess.call(["coverage3", "combine"])
        subprocess.call(["coverage3", "report", "-m"])
        if self.args.html:
            shutil.rmtree(".htmlreport", ignore_errors=True)
            print("Generating HTML report to .htmlreport...")
            subprocess.call(["coverage3", "html", "-d", ".htmlreport"])
            try:
                webbrowser.open_new_tab(os.path.join(".htmlreport",
                                                     "index.html"))
            except webbrowser.Error:
                pass

    def __print_output(self, command_array):
        p = subprocess.Popen(command_array,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             universal_newlines=True)
        retval = p.wait()
        if retval != 0 or self.args.verbose:
            for line in p.stderr:
                print(line, end='')
            for line in p.stdout:
                print(line, end='')

        return retval

    def __execute_python3_file(self, filename, ignored_files):
        # On windows we won't find a python3 executable and don't use coverage
        if sys.platform.startswith("win"):
            return self.__print_output(["python", filename])

        if not self.args.cover:
            return self.__print_output(["python3", filename])

        return self.__print_output(["coverage3",
                                    "run",
                                    "-p",  # make it collectable later
                                    "--branch",
                                    "--omit",
                                    ignored_files,
                                    filename])

    @staticmethod
    def __check_module_skip(filename):
        module_dir = os.path.dirname(filename)
        if module_dir not in sys.path:
            sys.path.insert(0, module_dir)

        # Don't allow module code printing
        with suppress_stdout():
            module = importlib.import_module(
                os.path.basename(os.path.splitext(filename)[0]))

        for name, object in inspect.getmembers(module):
            if inspect.isfunction(object) and name == "skip_test":
                return object()

        return False

    def __execute_test(self, filename, curr_nr, max_nr, ignored_files):
        """
        Executes the given test and counts up failed_tests or skipped_tests if
        needed.

        :param filename: Filename of test to execute
        :param curr_nr: Number of current test
        :param max_nr: Count of all tests
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
