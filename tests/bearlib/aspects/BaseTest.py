from coalib.bearlib.aspects import aspectclass
from coalib.bearlib.aspects.base import aspectbase

import pytest


class AspectBaseTest:
    """
    aspectbase is just a mixin base class for new aspectclasses
    and is therefore only usable works with a derived aspectclass
    and therefore doesn't use the aspectclass meta for itself
    """

    def test_class(self):
        assert not isinstance(aspectbase, aspectclass)

    def test_init_needs_aspectclass(self):
        with pytest.raises(AttributeError):
            aspectbase('py')
