# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License
# for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from coalib.coala_main import run_coala
from coalib.output.ConsoleInteraction import print_results_formatted


def main():
    results, exitcode, _ = run_coala(print_results=print_results_formatted)

    return exitcode


if __name__ == '__main__':  # pragma: no cover
    main()
