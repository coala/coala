import pytest
import unittest

from coalib.bearlib.aspects import (
    AspectNotFoundError, AspectTypeError as aspectTypeError)
from coalib.bearlib.aspects.collections import AspectList
from coalib.bearlib.aspects.meta import isaspect
from coalib.bearlib.aspects.Metadata import Metadata


class AspectListTest(unittest.TestCase):

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
