import os
import subprocess
import sys
import shutil
import webbrowser


class TestHelper:
    @staticmethod
    def __show_coverage_results(generate_html_coverage=False):
        subprocess.call(["coverage3", "combine"])
        subprocess.call(["coverage3", "report", "-m"])
        if generate_html_coverage:
            shutil.rmtree(".htmlreport", ignore_errors=True)
            print("Generating HTML report to .htmlreport...")
            subprocess.call(["coverage3", "html", "-d", ".htmlreport"])
            try:
                webbrowser.open_new_tab(os.path.join(".htmlreport", "index.html"))
            except webbrowser.Error:
                pass

    @staticmethod
    def __delete_previous_coverage():
        """
        :return: False if coverage3 cannot be executed.
        """
        try:
            subprocess.call(["coverage3", "erase"])
            return True
        except:
            print("Coverage failed. Falling back to standard unit tests.")
            return False

    @staticmethod
    def print_output(command_array, verbose):
        p = subprocess.Popen(command_array, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        retval = p.wait()
        if retval != 0 or verbose:
            for line in p.stderr:
                print(line, end='')
            for line in p.stdout:
                print(line, end='')

        return retval

    @staticmethod
    def execute_python3_file(filename, use_coverage, ignored_files, verbose):
        if sys.platform.startswith("win"):
            # On windows we won't find a python3 executable and we don't measure coverage
            return TestHelper.print_output(["python", filename], verbose)

        if not use_coverage:
            return TestHelper.print_output(["python3", filename], verbose)

        return TestHelper.print_output(["coverage3",
                                        "run",
                                        "-p",  # make it collectable later
                                        "--branch",  # check branch AND statement coverage
                                        "--omit",
                                        ignored_files,
                                        filename], verbose)

    @staticmethod
    def execute_python3_files(filenames, use_coverage, ignore_list, verbose=False, generate_html_coverage=False):
        if use_coverage:
            use_coverage = TestHelper.__delete_previous_coverage()  # Don't use coverage if this fails

        number = len(filenames)
        failures = 0
        for i, file in enumerate(filenames):
            print(" {:>2}/{:<2} | {}".format(i+1, number, os.path.splitext(os.path.basename(file))[0]))
            result = TestHelper.execute_python3_file(file, use_coverage, ",".join(ignore_list), verbose)  # either 0 or 1
            failures += result
            if verbose or result != 0:
                print("#" * 70)

        print("\nTests finished: failures in {} of {} test modules".format(failures, number))

        if use_coverage:
            TestHelper.__show_coverage_results(generate_html_coverage)

        return failures

    @staticmethod
    def get_test_files(testdir, omit_names, test_only):
        test_files = []
        for (dirpath, dirnames, filenames) in os.walk(testdir):
            for filename in filenames:
                if TestHelper.is_eligible_test(filename, omit_names, test_only):
                    test_files.append(os.path.join(dirpath, filename))
        return test_files

    @staticmethod
    def is_eligible_test(filename, omit_names, test_only):
        if not filename.endswith("Test.py"):
            return False
        name = os.path.splitext(os.path.basename(filename))[0]
        if omit_names is not None and name in omit_names:
            return False
        if test_only is not None and name not in test_only:
            return False

        return True
