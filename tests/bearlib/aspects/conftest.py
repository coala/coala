from coalib.bearlib.aspects import Taste, aspectclass
from coalib.bearlib.aspects.base import aspectbase

import coalib.bearlib.aspects.Metadata
import coalib.bearlib.aspects.Redundancy

import pytest


@pytest.fixture
def RootAspect():
    """
    An exclusive Root aspectclass for unit tests.
    """
    class RootAspect(aspectbase, metaclass=aspectclass):
        parent = None

        _tastes = {}

    return RootAspect


@pytest.fixture
def SubAspect_tastes():
    """
    Taste definitions for an exclusive SubAspect class for unit tests.
    """
    return {
        'salty': Taste[str](
            'The saltiness', ('high', 'low'), default='low'),
        'sweet': Taste[int](
            'The sweetness', (1, 23, 45), default=23,
            languages=('py', )),
        'sour': Taste[bool](
            'Is it sour?', (True, False), default=False),
    }


@pytest.fixture
def SubAspect_taste_values():
    """
    Taste definitions for an exclusive SubAspect class for unit tests.
    """
    return {
        'salty': 'high',
        'sweet': 45,
        'sour': True,
    }


@pytest.fixture
def SubAspect_docs():
    """
    Docs definitions for an exclusive SubAspect class for unit tests.
    """
    class docs:
        example = 'An example'
        example_language = 'The example language'
        importance_reason = 'The reason of importance'
        fix_suggestions = 'Suggestions for fixing'

    return docs


@pytest.fixture
def SubAspect(RootAspect, SubAspect_docs, SubAspect_tastes):
    """
    An exclusive SubAspect class for unit tests.
    """
    @RootAspect.subaspect
    class SubAspect:
        """
        Definition
        """
        docs = SubAspect_docs

        salty = SubAspect_tastes['salty']
        sweet = SubAspect_tastes['sweet']
        sour = SubAspect_tastes['sour']

    return SubAspect
