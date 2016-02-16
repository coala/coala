from queue import Queue

from bears.general.SpaceConsistencyBear import (
    SpaceConsistencyBear, SpacingHelper)
from bears.tests.LocalBearTestHelper import LocalBearTestHelper
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


class SpaceConsistencyBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section("test section")
        self.uut = SpaceConsistencyBear(self.section, Queue())

    def test_needed_settings(self):
        self.section.append(Setting("use_spaces", "true"))

        needed_settings = self.uut.get_non_optional_settings()
        self.assertEqual(len(needed_settings),
                         1 + len(SpacingHelper.get_non_optional_settings()))
        self.assertIn("use_spaces", needed_settings)

    def test_defaults(self):
        # use_spaces is no default, need to set it explicitly.
        self.section.append(Setting("use_spaces", "true"))

        self.check_validity(self.uut, "    t")
        self.check_validity(self.uut, "\tt", valid=False)
        self.check_validity(self.uut, "t \n", valid=False)
        self.check_validity(self.uut, "t", force_linebreaks=False, valid=False)

    def test_data_sets_spaces(self):
        self.section.append(Setting("use_spaces", "true"))
        self.section.append(Setting("allow_trailing_whitespace", "false"))
        self.section.append(Setting("enforce_newline_at_EOF", "false"))

        self.check_validity(self.uut, "    t")
        self.check_validity(self.uut, "t \n", valid=False)
        self.check_validity(self.uut, "\tt\n", valid=False)

    def test_data_sets_tabs(self):
        self.section.append(Setting("use_spaces", "false"))
        self.section.append(Setting("allow_trailing_whitespace", "true"))
        self.section.append(Setting("enforce_newline_at_EOF", "false"))

        self.check_validity(self.uut, "    t", valid=False)
        self.check_validity(self.uut, "t \n")
        self.check_validity(self.uut, "\tt\n")

    def test_enforce_newline_at_eof(self):
        self.section.append(Setting("use_spaces", "true"))
        self.section.append(Setting("allow_trailing_whitespace", "true"))
        self.section.append(Setting("enforce_newline_at_EOF", "true"))

        self.check_validity(self.uut, "hello world  \n", force_linebreaks=False)
        self.check_validity(self.uut,
                            ["def somecode():\n",
                             "    print('funny')\n",
                             "    print('funny end.')\n"],
                            force_linebreaks=False)
        self.check_validity(self.uut,
                            " no hello world",
                            force_linebreaks=False,
                            valid=False)
        self.check_validity(self.uut,
                            ["def unfunny_code():\n",
                             "    print('funny')\n",
                             "    print('the result is not funny...')"],
                            force_linebreaks=False,
                            valid=False)
