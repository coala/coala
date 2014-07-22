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


class TestHelper:
    @staticmethod
    def execute_python3_file(filename):
        return subprocess.call(["python3", filename])

    @staticmethod
    def execute_python3_files(filenames):
        number = len(filenames)
        failures = 0
        retval = 0
        for file in filenames:
            print("\nRunning: {} ({})\n".format(os.path.splitext(os.path.basename(file))[0], file), end='')
            result = TestHelper.execute_python3_file(file)  # either 0 or 1
            failures += result
            retval = max(result, retval)
            print("\n"+"#"*70)

        print("\nTests finished: failures in {} of {} test modules".format(failures, number))
        return retval

    @staticmethod
    def get_test_files(testdir):
        test_files = []
        for (dirpath, dirnames, filenames) in os.walk(testdir):
            for filename in filenames:
                if filename.endswith("Test.py"):
                    test_files.append(os.path.join(dirpath, filename))
        return test_files
