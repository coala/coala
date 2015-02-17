import sys
sys.path.insert(0, ".")
import unittest
from coalib.settings.Section import Section
from coalib.bearlib.spacing.SpacingHelper import SpacingHelper
from coalib.settings.Setting import Setting


class SpacingHelperTestCase(unittest.TestCase):
    def setUp(self):
        self.uut = SpacingHelper()

    def test_needed_settings(self):
        self.assertEqual(list(self.uut.get_optional_settings()), ["tab_width"])
        self.assertEqual(list(self.uut.get_non_optional_settings()), [])

    def test_construction(self):
        section = Section("test section")
        self.assertRaises(TypeError, SpacingHelper, "no integer")
        self.assertRaises(TypeError, self.uut.from_section, 5)

        self.assertEqual(self.uut.tab_width, self.uut.from_section(section).tab_width)

        section.append(Setting("tab_width", "invalid"))
        # Setting won't be converted since it's not possible, SpacingHelper
        # will then complain with TypeError
        self.assertRaises(TypeError, self.uut.from_section, section)

        # This is assumed in some tests. If you want to change this value, be
        # sure to change the tests too
        self.assertEqual(self.uut.DEFAULT_TAB_WIDTH, 4)
        self.assertEqual(self.uut.tab_width, self.uut.DEFAULT_TAB_WIDTH)

    def test_get_indentation(self):
        self.assertRaises(TypeError, self.uut.get_indentation, 5)

        self.assertEqual(self.uut.get_indentation("no indentation"), 0)
        self.assertEqual(self.uut.get_indentation(" indentation"), 1)
        self.assertEqual(self.uut.get_indentation("  indentation"), 2)
        self.assertEqual(self.uut.get_indentation("\tindentation"), self.uut.DEFAULT_TAB_WIDTH)

        # Having a space before the tab shouldn't make any difference
        self.assertEqual(self.uut.get_indentation(" \tindentation"), self.uut.DEFAULT_TAB_WIDTH)
        self.assertEqual(self.uut.get_indentation(" \t indentation"), self.uut.DEFAULT_TAB_WIDTH+1)
        self.assertEqual(self.uut.get_indentation("\t indentation"), self.uut.DEFAULT_TAB_WIDTH+1)

        # same tests but with indentation only
        self.assertEqual(self.uut.get_indentation("\t"), self.uut.DEFAULT_TAB_WIDTH)
        self.assertEqual(self.uut.get_indentation(" \t"), self.uut.DEFAULT_TAB_WIDTH)
        self.assertEqual(self.uut.get_indentation(" \t "), self.uut.DEFAULT_TAB_WIDTH+1)
        self.assertEqual(self.uut.get_indentation("\t "), self.uut.DEFAULT_TAB_WIDTH+1)
        self.assertEqual(self.uut.get_indentation("\t\t"), self.uut.DEFAULT_TAB_WIDTH*2)

    def test_replace_tabs_with_spaces(self):
        self.assertRaises(TypeError, self.uut.replace_tabs_with_spaces, 5)

        self.assertEqual(self.uut.replace_tabs_with_spaces(""), "")
        self.assertEqual(self.uut.replace_tabs_with_spaces(" "), " ")
        self.assertEqual(self.uut.replace_tabs_with_spaces("\t"), " "*self.uut.DEFAULT_TAB_WIDTH)
        self.assertEqual(self.uut.replace_tabs_with_spaces("\t\t"), " "*self.uut.DEFAULT_TAB_WIDTH*2)
        self.assertEqual(self.uut.replace_tabs_with_spaces(" \t"), " "*self.uut.DEFAULT_TAB_WIDTH)
        self.assertEqual(self.uut.replace_tabs_with_spaces("  \t"), " "*self.uut.DEFAULT_TAB_WIDTH)
        self.assertEqual(self.uut.replace_tabs_with_spaces("d \t "), "d" + " "*self.uut.DEFAULT_TAB_WIDTH)

    def test_replace_spaces_with_tabs(self):
        self.assertRaises(TypeError, self.uut.replace_spaces_with_tabs, 5)

        self.assertEqual(self.uut.replace_spaces_with_tabs(""), "")
        self.assertEqual(self.uut.replace_spaces_with_tabs(" "), " ")
        self.assertEqual(self.uut.replace_spaces_with_tabs("    "), "\t")
        self.assertEqual(self.uut.replace_spaces_with_tabs("   \t"), "\t")
        self.assertEqual(self.uut.replace_spaces_with_tabs("   dd  "), "   dd  ")
        self.assertEqual(self.uut.replace_spaces_with_tabs("   dd d "), "   dd d ")  # One space shouldnt be replaced
        self.assertEqual(self.uut.replace_spaces_with_tabs("   dd   "), "   dd\t")
        self.assertEqual(self.uut.replace_spaces_with_tabs(" \t   a_text   another"), "\t   a_text\tanother")
        self.assertEqual(self.uut.replace_spaces_with_tabs("d  d"), "d  d")


if __name__ == '__main__':
    unittest.main(verbosity=2)
