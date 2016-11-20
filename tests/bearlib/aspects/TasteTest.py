from coalib.bearlib.aspects import Taste
from coalib.bearlib.aspects.taste import TasteMeta


class TasteTest:

    def test_class(self):
        assert isinstance(Taste, TasteMeta)

    def test_class__getitem__(self):
        typed = Taste[int]
        assert typed.cast_type is int
        assert typed.__name__ == typed.__qualname__ == 'Taste[int]'

    def test__init__defaults(self):
        taste = Taste()
        assert taste.description is ''
        assert taste.suggested_values is ()
        assert taste.default is None

    def test__get__(
            self, SubAspect, SubAspect_tastes, SubAspect_taste_values
    ):
        using_default_values = SubAspect('py')
        using_custom_values = SubAspect('py', **SubAspect_taste_values)
        for name, taste in SubAspect_tastes.items():
            assert getattr(SubAspect, name) is taste
            assert getattr(using_default_values, name) == taste.default
            assert getattr(using_custom_values, name) \
                == SubAspect_taste_values[name]
