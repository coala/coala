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
import sys

sys.path.append(".")
import unittest
from coalib.internal.modifying.Merger import Merger


class MergerTestCase(unittest.TestCase):
    def setUp(self):
        self.m_keep = Merger(1)
        self.m_none = Merger(0)
        self.m_discard = Merger(-1)

    def test_conflictless_three_way_merge(self):
        merge_sets = [
            ["abc", "abc", "abc"],
            ["abc", "aabc", "aabc"],
            ["abc", "aabc", "abbc"],
            ["abc", "bc", "bc"],
            ["abc", "bc", "ac"],
            ["abc", "ac", "bbc"],

            ["abc", "a\u2192c", "\nbc"],
            ["€@$", "€@@$", "€€@$"],
            ["ab\n", "b\n", "ab\n\n"],
            ["a", "", ""],
            [".........1.........2.........3.........4.........5........6.........7..........8.........9........10\
             ........11........12........13........14........15........16........17........18........19.........20",
             "..................2.........3.........4.........5........6.........7..........8.........9........10\
             ........11........12........13........14........15........16........17........18........19.........20",
             "..."]
        ]

        results = [
            "abc",
            "aabc",
            "aabbc",
            "bc",
            "c",
            "bc",
            "\n\u2192c",
            "€€@@$",
            "b\n\n",
            "",
            "..."
        ]

        for i in range(len(merge_sets)):
            m_keep_result, m_keep_conflicts = self.m_keep.three_way_merge(merge_sets[i][0],
                                                                          merge_sets[i][1],
                                                                          merge_sets[i][2])
            m_none_result, m_none_conflicts = self.m_none.three_way_merge(merge_sets[i][0],
                                                                          merge_sets[i][1],
                                                                          merge_sets[i][2])
            m_discard_result, m_discard_conflicts = self.m_discard.three_way_merge(merge_sets[i][0],
                                                                                   merge_sets[i][1],
                                                                                   merge_sets[i][2])
            expected_result = results[i]

            self.assertEqual(m_keep_result,
                             expected_result,
                             "Merger(1).__three_way_merge({},{},{}) returns {} instead of {}".format(merge_sets[i][0],
                                                                                                     merge_sets[i][1],
                                                                                                     merge_sets[i][2],
                                                                                                     m_keep_result,
                                                                                                     expected_result))
            self.assertEqual(m_none_result,
                             expected_result,
                             "Merger(0).__three_way_merge({},{},{}) returns {} instead of {}".format(merge_sets[i][0],
                                                                                                     merge_sets[i][1],
                                                                                                     merge_sets[i][2],
                                                                                                     m_none_result,
                                                                                                     expected_result))
            self.assertEqual(m_discard_result,
                             expected_result,
                             "Merger(-1).__three_way_merge({},{},{}) returns {} instead of {}".format(merge_sets[i][0],
                                                                                                      merge_sets[i][1],
                                                                                                      merge_sets[i][2],
                                                                                                      m_discard_result,
                                                                                                      expected_result))
            self.assertFalse(m_keep_conflicts,
                             "Merger(1).__three_way_merge conflicts on {} although it shouldn't".format(merge_sets[i]))
            self.assertFalse(m_none_conflicts,
                             "Merger(0).__three_way_merge conflicts on {} although it shouldn't".format(merge_sets[i]))
            self.assertFalse(m_discard_conflicts,
                             "Merger(-1).__three_way_merge conflicts on {} although it shouldn't".format(merge_sets[i]))

if __name__ == '__main__':
    unittest.main()
