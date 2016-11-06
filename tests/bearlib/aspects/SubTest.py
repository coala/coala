from coalib.bearlib.aspects import Root, aspectclass
from coalib.bearlib.aspects.base import aspectbase


class SubAspectTest:

    def test_class(self, SubAspect):
        assert isinstance(SubAspect, aspectclass)
        assert issubclass(SubAspect, aspectbase)

    def test_class_tastes_recreation(self, SubAspect):
        assert SubAspect.tastes is not SubAspect.tastes

    def test_class_tastes_items(self, SubAspect, SubAspect_tastes):
        tastes = SubAspect.tastes
        for name, taste in SubAspect_tastes.items():
            assert taste is tastes.pop(name)
        assert not tastes

    def test__eq__(self, RootAspect, SubAspect, SubAspect_taste_values):
        assert SubAspect() == SubAspect()
        assert SubAspect(**SubAspect_taste_values) \
            == SubAspect(**SubAspect_taste_values)
        assert not SubAspect() == RootAspect()
        assert not SubAspect() == Root()
        assert not SubAspect() == SubAspect(**SubAspect_taste_values)
        assert not SubAspect(**SubAspect_taste_values) == SubAspect()

    def test__ne__(self, RootAspect, SubAspect, SubAspect_taste_values):
        assert not SubAspect() != SubAspect()
        assert not SubAspect(**SubAspect_taste_values) \
            != SubAspect(**SubAspect_taste_values)
        assert SubAspect() != RootAspect()
        assert SubAspect() != Root()
        assert SubAspect() != SubAspect(**SubAspect_taste_values)
        assert SubAspect(**SubAspect_taste_values) != SubAspect()
