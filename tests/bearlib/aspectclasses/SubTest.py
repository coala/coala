from coalib.bearlib.aspectclasses import aspectclass
from coalib.bearlib.aspectclasses.base import aspectbase


class SubAspectTest:

    def test_class(self, SubAspect):
        assert isinstance(SubAspect, aspectclass)
        assert issubclass(SubAspect, aspectbase)

    def test_tastes_recreation(self, SubAspect):
        assert SubAspect.tastes is not SubAspect.tastes

    def test_tastes_items(self, SubAspect, SubAspect_tastes):
        tastes = SubAspect.tastes
        for name, taste in SubAspect_tastes.items():
            assert taste is tastes.pop(name)
        assert not tastes
