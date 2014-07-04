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
    def execute_python_file(filename):
        return subprocess.call(["python", filename])

    @staticmethod
    def execute_python_files(filenames):
        retval = 0
        for file in filenames:
            retval = max(TestHelper.execute_python_file(file), retval)
        return retval

    @staticmethod
    def join_paths(prefix, paths):
        result = []
        for path in paths:
            result.append(os.path.join(prefix, path))
        return result
