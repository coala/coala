import pytest
import unittest

from coalib.bearlib.aspects import (
    AspectNotFoundError, AspectTypeError as aspectTypeError)
from coalib.bearlib.aspects.collections import AspectList
from coalib.bearlib.aspects.meta import isaspect
from coalib.bearlib.aspects.Metadata import Metadata
from coalib.bearlib.aspects.Redundancy import Redundancy
from coalib.bears.LocalBear import LocalBear


class AspectListTest(unittest.TestCase):

    def setUp(self):
        self.aspectlist_excludes = AspectList(
            seq=[Metadata.CommitMessage.Shortlog,
                 Metadata.CommitMessage.Body],
            exclude=[Metadata.CommitMessage.Shortlog.TrailingPeriod,
                     Metadata.CommitMessage.Body.Existence])
        self.instancelist_excludes = AspectList(
            seq=[Metadata.CommitMessage.Shortlog('py'),
                 Metadata.CommitMessage.Body('py')],
            exclude=[Metadata.CommitMessage.Shortlog.TrailingPeriod,
                     Metadata.CommitMessage.Body.Existence])
        self.unused_variable_leaves = AspectList([
            Redundancy.UnusedVariable.UnusedGlobalVariable,
            Redundancy.UnusedVariable.UnusedLocalVariable,
            Redundancy.UnusedVariable.UnusedParameter,
        ])

    def test__init__(self):
        list_of_aspect = AspectList(['CommitMessage.Shortlog',
                                     'CommitMessage.Body'])
        mix_of_aspect = AspectList(['CommitMessage.Shortlog',
                                    Metadata.CommitMessage.Body])
        self.assertIsInstance(list_of_aspect, AspectList)
        self.assertIs(list_of_aspect[0], Metadata.CommitMessage.Shortlog)
        self.assertIs(list_of_aspect[1], Metadata.CommitMessage.Body)
        self.assertEqual(list_of_aspect, mix_of_aspect)

        with self.assertRaisesRegex(AspectNotFoundError,
                                    "^No aspect named 'String'$"):
            AspectList(['String'])

    def test__contains__(self):
        list_of_aspect = AspectList(
            [Metadata.CommitMessage.Shortlog, Metadata.CommitMessage.Body])
        assert Metadata.CommitMessage.Shortlog in list_of_aspect
        assert Metadata.CommitMessage.Shortlog.ColonExistence in list_of_aspect
        assert Metadata.CommitMessage.Body in list_of_aspect
        assert Metadata not in list_of_aspect
        assert Metadata.CommitMessage.Emptiness not in list_of_aspect

        with pytest.raises(aspectTypeError) as exc:
            'Metadata.CommitMessage.Shortlog' in list_of_aspect
        assert not isaspect('Metadata.CommitMessage.Shortlog')
        exc.match("'Metadata.CommitMessage.Shortlog' is not an "
                  'aspectclass or an instance of an aspectclass')
        with pytest.raises(aspectTypeError) as exc:
            str in list_of_aspect
        assert not isaspect(str)
        exc.match("<class 'str'> is not an "
                  'aspectclass or an instance of an aspectclass')

    def test__contains__excludes(self):
        self.assertIn(Metadata.CommitMessage.Shortlog.ColonExistence,
                      self.aspectlist_excludes)
        self.assertNotIn(Metadata.CommitMessage.Shortlog.TrailingPeriod,
                         self.aspectlist_excludes)
        self.assertNotIn(Metadata.CommitMessage.Body.Existence,
                         self.aspectlist_excludes)

    def test_bear__contains__(self):
        class aspectsTestBear(LocalBear, aspects={
                    'detect': [Metadata.CommitMessage.Shortlog],
                    'fix': [Metadata.CommitMessage.Shortlog.TrailingPeriod]
                }, languages=['Python', 'Vala']):
            pass

        aspectClass = Metadata.CommitMessage.Shortlog
        aspectInstance1 = Metadata.CommitMessage.Shortlog('Python')
        aspectInstance2 = Metadata.CommitMessage.Shortlog('C#')
        self.assertIn(aspectClass, aspectsTestBear.aspects['detect'])
        self.assertIn(aspectInstance1, aspectsTestBear.aspects['detect'])
        self.assertNotIn(aspectInstance2, aspectsTestBear.aspects['detect'])

    def test_get(self):
        list_of_aspect = AspectList(
            [Metadata.CommitMessage.Shortlog, Metadata.CommitMessage.Body])
        self.assertIs(list_of_aspect.get(Metadata.CommitMessage.Shortlog),
                      Metadata.CommitMessage.Shortlog)
        self.assertIs(list_of_aspect.get(Metadata.CommitMessage.Body.Length),
                      Metadata.CommitMessage.Body.Length)
        self.assertIs(list_of_aspect.get('Body.Length'),
                      Metadata.CommitMessage.Body.Length)
        self.assertIsNone(list_of_aspect.get(Metadata))

    def test_get_excludes(self):
        CommitMessage = Metadata.CommitMessage
        ColonExistence = Metadata.CommitMessage.Shortlog.ColonExistence

        self.assertIs(self.aspectlist_excludes.get(ColonExistence),
                      ColonExistence)
        self.assertIsNone(self.aspectlist_excludes.get(
                          CommitMessage.Shortlog.TrailingPeriod))
        self.assertIsNone(self.aspectlist_excludes.get(
                          CommitMessage.Body.Existence))

        self.assertEqual(self.instancelist_excludes.get(ColonExistence),
                         ColonExistence('py'))
        self.assertIsNone(self.instancelist_excludes.get(
                          CommitMessage.Shortlog.TrailingPeriod))
        self.assertIsNone(self.instancelist_excludes.get(
                          CommitMessage.Body.Existence))

    def test_get_leaf_aspects(self):
        leaves = AspectList([
            Metadata.CommitMessage.Body.Length('py'),
            Metadata.CommitMessage.Shortlog.ColonExistence('py'),
            Metadata.CommitMessage.Shortlog.FirstCharacter('py'),
            Metadata.CommitMessage.Shortlog.Length('py'),
            Metadata.CommitMessage.Shortlog.Tense('py'),
        ])
        instancelist_leaf = self.instancelist_excludes.get_leaf_aspects()

        self.assertCountEqual(instancelist_leaf, leaves)

    def test_get_leaf_aspects_duplicated_node(self):
        aspects = AspectList([
            Redundancy.UnusedVariable,
            Redundancy.UnusedVariable.UnusedLocalVariable,
        ]).get_leaf_aspects()

        self.assertCountEqual(aspects, self.unused_variable_leaves)

    def test_get_leaf_aspects_irrelevant_exclude(self):
        aspects = AspectList([Redundancy.UnusedVariable],
                             exclude=[Metadata]).get_leaf_aspects()

        self.assertCountEqual(aspects, self.unused_variable_leaves)

    def test_remove(self):
        aspectlist = AspectList([Metadata.CommitMessage])
        self.assertIn(Metadata.CommitMessage, aspectlist)

        with self.assertRaisesRegex(
                ValueError,
                "^AspectList._remove\(x\): <aspectclass 'Root.Metadata'> "
                'not in list.$'):
            aspectlist._remove(Metadata)

        aspectlist._remove(Metadata.CommitMessage)
        self.assertEqual(aspectlist, AspectList())
