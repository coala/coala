import unittest

from coalib.bearlib.aspects import (
    AspectList,
    get as get_aspect,
    map_setting_to_aspect,
)
from coalib.bears.LocalBear import LocalBear
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


class RunDecoratedBear(LocalBear):

    @map_setting_to_aspect(
        remove_unreachable_code=get_aspect('UnreachableCode'),
        minimum_clone_tokens=get_aspect('Clone').min_clone_tokens,
    )
    def run(self,
            remove_unreachable_code: bool=False,
            minimum_clone_tokens: int=10,
            ):
        return [remove_unreachable_code, minimum_clone_tokens]


class MapSettingToAspectTest(unittest.TestCase):

    def setUp(self):
        self.section = Section('aspect section')
        self.bear = RunDecoratedBear(self.section, None)

    def test_mapping(self):
        self.section.aspects = AspectList([
            get_aspect('UnreachableCode')('py'),
            get_aspect('Clone')('py', min_clone_tokens=30),
        ])
        result = self.bear.execute()
        self.assertEqual([True, 30], result)

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
        self.assertEqual([False, 40], result)

    def test_partial_mapping(self):
        self.section.aspects = AspectList([
            get_aspect('UnreachableCode')('py'),
        ])
        result = self.bear.execute()
        self.assertEqual([True, 10], result)

    def test_no_mapping(self):
        self.section.aspects = AspectList([])
        result = self.bear.execute()
        self.assertEqual([False, 10], result)

    def test_skip_mapping(self):
        self.section.aspects = None
        result = self.bear.execute()
        self.assertEqual([False, 10], result)
