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
import queue
from codeclib.fillib.filters.FilterBase import FILTER_KIND
from codeclib.internal.process_managing.Process import Process


class ResultContainer:
    def __init__(self):
        self.result_list = []

    def add(self, other):
        return self.__add__(other)

    def append(self, other):
        return self.__add__(other)

    def __add__(self, other):
        return self.result_list.append(other)
