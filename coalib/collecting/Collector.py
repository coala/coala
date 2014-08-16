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
from coalib.misc.i18n import _


class Collector:
    def __init__(self):
        self._items = None

    def collect(self):
        raise NotImplementedError

    def __iter__(self):
        self._check_item_availability()
        return iter(self._items)

    def __len__(self):
        self._check_item_availability()
        return len(self._items)

    def __getitem__(self, item):
        self._check_item_availability()
        return self._items[item]

    def __reversed__(self):
        self._check_item_availability()
        return reversed(self._items)

    def _check_item_availability(self):
        if self._items is None:
            raise ValueError(_("collector must collect items before they can be accessed"))
