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
from functools import total_ordering
from coalib.bears.results.RESULT_SEVERITY import RESULT_SEVERITY


@total_ordering
class Result:
    """
    A result is anything that has an origin and a message.

    Optionally it might affect a file.

    When sorting a list of results with the implemented comparision routines you will get an ordering which follows the
    following conditions, while the first condition has the highest priority, which descends to the last condition.
    1. Results with no files will be shown first
    2. Results will be sorted by files (ascending alphabetically)
    3. Results will be sorted by severity (descending, major first, info last)
    4. Results will be sorted by origin (ascending alphabetically)
    5. Results will be sorted by message (ascending alphabetically)
    """

    def __init__(self, origin, message, file=None, severity=RESULT_SEVERITY.NORMAL):
        """
        :param origin: Class name of the creator of this object
        :param file: The path to the affected file
        """
        self.origin = origin
        self.message = message
        self.file = file
        self.severity = severity

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "Result:\n origin: '{origin}'\n file: '{file}'\n severity: {severity}\n" \
               "'{msg}'".format(origin=self.origin, file=self.file, severity=self.severity, msg=self.message)

    def __eq__(self, other):
        return isinstance(other, Result) and \
               self.origin == other.origin and \
               self.message == other.message and \
               self.file == other.file and \
               self.severity == other.severity

    def __lt__(self, other):
        if not isinstance(other, Result):
            raise TypeError("Comparision with non-result classes is not supported.")

        # Show elements without files first
        if (self.file is None) != (other.file is None):
            return self.file is None

        # Now either both .file members are None or both are set
        if self.file != other.file:
            return self.file < other.file

        # Both files are equal
        if self.severity != other.severity:
            return self.severity > other.severity

        # Severities are equal, files are equal
        if self.origin != other.origin:
            return self.origin < other.origin

        return self.message < other.message
