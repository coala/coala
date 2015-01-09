"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import os
import subprocess
import tempfile
import sys
from distutils.sysconfig import get_python_lib


class TestHelper:
    @staticmethod
    def __show_coverage_results():
        try:
            subprocess.call(["coverage3", "combine"])
            subprocess.call(["coverage3", "report", "-m"])
        except:
            pass

    @staticmethod
    def execute_python3_file(filename, use_coverage):
        if sys.platform.startswith("win"):
            # On windows we won't find a python3 executable and we don't measure coverage
            return subprocess.call(["python", filename])

        if not use_coverage:
            return subprocess.call(["python3", filename])

        try:
            return subprocess.call(["coverage3",
                                    "run",
                                    "-p",  # make it collectable later
                                    "--branch",  # check branch AND statement coverage
                                    "--omit",  # dont check coverage of test file itself
                                    filename + "," + os.path.join(tempfile.gettempdir(), "*") +
                                    "," + os.path.join(get_python_lib(), "*"),
                                    filename])
        except:
            print("Coverage failed. Falling back to standard unit tests.")
            return subprocess.call(["python3", filename])

    @staticmethod
    def execute_python3_files(filenames, use_coverage=False):
        number = len(filenames)
        failures = 0
        for file in filenames:
            print("\nRunning: {} ({})\n".format(os.path.splitext(os.path.basename(file))[0], file), end='')
            result = TestHelper.execute_python3_file(file, use_coverage)  # either 0 or 1
            failures += result
            print("\n" + "#" * 70)

        print("\nTests finished: failures in {} of {} test modules".format(failures, number))

        if use_coverage:
            TestHelper.__show_coverage_results()

        return failures

    @staticmethod
    def get_test_files(testdir):
        test_files = []
        for (dirpath, dirnames, filenames) in os.walk(testdir):
            for filename in filenames:
                if filename.endswith("Test.py"):
                    test_files.append(os.path.join(dirpath, filename))
        return test_files
