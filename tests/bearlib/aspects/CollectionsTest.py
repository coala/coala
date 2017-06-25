import pytest

from coalib.bearlib.aspects import AspectTypeError as aspectTypeError
from coalib.bearlib.aspects.collections import AspectList
from coalib.bearlib.aspects.meta import isaspect
from coalib.bearlib.aspects.Metadata import Metadata


class AspectListTest:

    def test__init__(self):
        with pytest.raises(aspectTypeError) as exc:
            AspectList(['String'])
        exc.match("'String' is not an aspectclass or "
                  'an instance of an aspectclass')

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
