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
import time
from coalib.bears.LocalBear import LocalBear
from coalib.bears.results.Result import Result


class LocalTestBear(LocalBear):  # pragma: no cover
    def run_bear(self, filename, file):
        # we need to test that the SectionExecutor holds back the global results until processing of all local ones is
        # finished
        time.sleep(0.05)
        return [Result("LocalTestBear", "test message")]
