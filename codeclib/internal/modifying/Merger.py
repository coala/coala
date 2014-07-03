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

import difflib


class Merger:

    @staticmethod
    def drop_deltas(diff):
        result = []
        for item in diff:
            if not item.startswith('?'):
                result.append(item)
        return result

    def __init__(self, default_on_conflict=1):
        self.default_on_conflict = default_on_conflict

    def merge(self, original, *args):
        arg_list = list(args)
        modifications = arg_list
        conflicts = False

        if len(modifications) == 0:
            result = original
        elif len(modifications) == 1:
            result = modifications[0]
        else:
            interim_result = modifications[0]
            for i in range(1, len(modifications)):
                interim_result, interim_conflicts = self.__three_way_merge(original, interim_result, modifications[i])
                conflicts = conflicts or interim_conflicts
            result = interim_result

        if self.default_on_conflict == 0 and conflicts:
            return None, conflicts
        else:
            return result, conflicts

    def __three_way_merge(self, original, a, b):
        merge_result = ""
        index_a = 0
        index_b = 0
        conflicts = False

        dxa = difflib.Differ()
        dxb = difflib.Differ()
        xa = Merger.drop_deltas(dxa.compare(original, a))
        xb = Merger.drop_deltas(dxb.compare(original, b))

        while (index_a < len(xa)) and (index_b < len(xb)):

            # no change on either side or addition on both
            if xa[index_a] == xb[index_b] and (xa[index_a].startswith(' ') or xa[index_a].startswith('+ ')):
                merge_result += xa[index_a][2:]
                index_a += 1
                index_b += 1
                continue

            # subtraction on matching character from either side or both
            if (xa[index_a][2:] == xb[index_b][2:]) and (xa[index_a].startswith('- ') or xb[index_b].startswith('- ')):
                index_a += 1
                index_b += 1
                continue

            # addition in a only
            if xa[index_a].startswith('+ ') and xb[index_b].startswith('  '):
                merge_result += xa[index_a][2:]
                index_a += 1
                continue

            # addition in b only
            if xb[index_b].startswith('+ ') and xa[index_a].startswith('  '):
                merge_result += xb[index_b][2:]
                index_b += 1
                continue

            # conflict!
            conflicts = True
            if self.default_on_conflict >= 0:
                while (index_a < len(xa)) and not xa[index_a].startswith('  '):
                    merge_result += xa[index_a][2:]
                    index_a += 1
                while (index_b < len(xb)) and not xb[index_b].startswith('  '):
                    index_b += 1
            else:
                while (index_a < len(xa)) and not xa[index_a].startswith('  '):
                    index_a += 1
                while (index_b < len(xb)) and not xb[index_b].startswith('  '):
                    merge_result += xb[index_b][2:]
                    index_b += 1

        # remaining chars - there is only either a or b left
        for i in range(len(xa) - index_a):
            merge_result += xa[index_a + i][2:]
        for i in range(len(xb) - index_b):
            merge_result += xb[index_b + i][2:]

        return merge_result, conflicts
