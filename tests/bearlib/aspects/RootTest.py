from coalib.bearlib.aspects import Root, aspectclass
from coalib.bearlib.aspects.base import aspectbase


class RootTest:

    def test_class(self):
        assert isinstance(Root, aspectclass)
        assert issubclass(Root, aspectbase)

    def test_class_subaspects(self):
        assert isinstance(Root.subaspects, dict)

    def test_class_parent(self):
        assert Root.parent is None

    def test_class_tastes(self):
        assert Root.tastes == {}

    def test__eq__(self, RootAspect):
        assert Root() == Root()
        assert not Root() == RootAspect()

    def test__ne__(self, RootAspect):
        assert not Root() != Root()
        assert Root() != RootAspect()
