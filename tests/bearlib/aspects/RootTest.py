from coalib.bearlib.aspects import Root, aspectclass
from coalib.bearlib.aspects.base import aspectbase


class RootTest:

    def test_class(self):
        assert isinstance(Root, aspectclass)
        assert issubclass(Root, aspectbase)

    def test_subaspects(self):
        assert isinstance(Root.subaspects, dict)

    def test_parent(self):
        assert Root.parent is None

    def test_tastes(self):
        assert Root.tastes == {}
