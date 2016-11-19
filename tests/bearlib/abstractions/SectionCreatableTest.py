import unittest

from coalib.bearlib.abstractions.SectionCreatable import SectionCreatable
from coalib.settings.Section import Section, Setting


class TestObject(SectionCreatable):

    def __init__(self,
                 setting_one: int,
                 raw_setting,
                 setting_two: bool=False,
                 setting_three: list=[1, 2],
                 opt_raw_set=5):
        SectionCreatable.__init__(self)
        assert isinstance(setting_one, int)
        assert isinstance(raw_setting, Setting)
        assert isinstance(setting_two, bool)
        assert isinstance(setting_three, list)
        assert isinstance(opt_raw_set, Setting) or isinstance(opt_raw_set, int)

        self.setting_one = setting_one
        self.raw_setting = raw_setting
        self.setting_two = setting_two
        self.setting_three = setting_three
        self.opt_raw_set = opt_raw_set


class SectionCreatableTest(unittest.TestCase):

    def test_api(self):
        uut = SectionCreatable()
        self.assertEqual(uut.get_non_optional_settings(), {})
        self.assertEqual(uut.get_optional_settings(), {})

    def test_needed_settings(self):
        self.assertEqual(sorted(list(TestObject.get_non_optional_settings())),
                         sorted(['setting_one', 'raw_setting']))
        self.assertEqual(
            sorted(list(TestObject.get_optional_settings())),
            sorted(['setting_two', 'setting_three', 'opt_raw_set']))

    def test_from_section(self):
        section = Section('name')
        section.append(Setting('setting_one', ' 5'))
        section.append(Setting('raw_setting', ' 5s'))
        uut = TestObject.from_section(section)
        self.assertEqual(uut.setting_one, 5)
        self.assertEqual(str(uut.raw_setting), '5s')
        self.assertEqual(uut.setting_two, False)
        self.assertEqual(uut.setting_three, [1, 2])
        self.assertEqual(str(uut.opt_raw_set), '5')

        section.append(Setting('setting_three', '2, 4'))
        section.append(Setting('opt_raw_set', 'tst ,'))
        uut = TestObject.from_section(section)
        self.assertEqual(uut.setting_one, 5)
        self.assertEqual(str(uut.raw_setting), '5s')
        self.assertEqual(uut.setting_two, False)
        self.assertEqual(uut.setting_three, ['2', '4'])
        self.assertEqual(str(uut.opt_raw_set), 'tst ,')
