import unittest

from coalib.bearlib.aspects import (
    AspectList,
    get as get_aspect,
    map_setting_to_aspect,
    map_ambiguous_setting_to_aspect,
)
from coalib.bears.LocalBear import LocalBear
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


class RunDecoratedBear(LocalBear):

    @map_setting_to_aspect(
        remove_unreachable_code=get_aspect('UnreachableCode'),
        minimum_clone_tokens=get_aspect('Clone').min_clone_tokens,
    )
    @map_ambiguous_setting_to_aspect(
        use_spaces=(get_aspect('Indentation').indent_type,
                    [('space', True), ('tab', False)]),
    )
    def run(self,
            remove_unreachable_code: bool = False,
            minimum_clone_tokens: int = 10,
            use_spaces: bool = True,
            ):
        return [('remove_unreachable_code', remove_unreachable_code),
                ('minimum_clone_tokens', minimum_clone_tokens),
                ('use_spaces', use_spaces),
                ]


class MapSettingToAspectTest(unittest.TestCase):

    EXPECTED = {'remove_unreachable_code': False,
                'minimum_clone_tokens': 10,
                'use_spaces': True,
                }

    def setUp(self):
        self.section = Section('aspect section')
        self.bear = RunDecoratedBear(self.section, None)

    def test_mapping(self):
        self.section.aspects = AspectList([
            get_aspect('UnreachableCode')('py'),
            get_aspect('Clone')('py', min_clone_tokens=30),
        ])
        result = self.bear.execute()
        expected = self.EXPECTED.copy()
        expected['remove_unreachable_code'] = True
        expected['minimum_clone_tokens'] = 30
        self.assertEqual(expected, dict(result))

    def test_setting_priority(self):
        self.section.aspects = AspectList([
            get_aspect('UnreachableCode')('py'),
            get_aspect('Clone')('py', min_clone_tokens=30),
        ])
        self.section.append(
            Setting('remove_unreachable_code', 'False'))
        self.section.append(
            Setting('minimum_clone_tokens', 40))
        result = self.bear.execute()
        expected = self.EXPECTED.copy()
        expected['minimum_clone_tokens'] = 40
        self.assertEqual(expected, dict(result))

    def test_partial_mapping(self):
        self.section.aspects = AspectList([
            get_aspect('UnreachableCode')('py'),
        ])
        result = self.bear.execute()
        expected = self.EXPECTED.copy()
        expected['remove_unreachable_code'] = True
        self.assertEqual(expected, dict(result))

    def test_no_mapping(self):
        self.section.aspects = AspectList([])
        result = self.bear.execute()
        expected = self.EXPECTED.copy()
        self.assertEqual(expected, dict(result))

    def test_skip_mapping(self):
        self.section.aspects = None
        result = self.bear.execute()
        expected = self.EXPECTED.copy()
        self.assertEqual(expected, dict(result))


class MapAmbiguousSettingToAspectTest(unittest.TestCase):

    EXPECTED = {'remove_unreachable_code': False,
                'minimum_clone_tokens': 10,
                'use_spaces': True,
                }

    def setUp(self):
        self.section = Section('aspect section')
        self.bear = RunDecoratedBear(self.section, None)

    def test_mapping(self):
        self.section.aspects = AspectList([
            get_aspect('Indentation')('py', indent_type='tab'),
        ])
        result = self.bear.execute()
        expected = self.EXPECTED.copy()
        expected['use_spaces'] = False
        self.assertEqual(expected, dict(result))

    def test_setting_priority(self):
        self.section.aspects = AspectList([
            get_aspect('Indentation')('py', indent_type='tab'),
        ])
        self.section.append(Setting('use_spaces', True))
        result = self.bear.execute()
        expected = self.EXPECTED.copy()
        self.assertEqual(expected, dict(result))
