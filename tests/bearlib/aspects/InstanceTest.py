from itertools import chain

import pytest


class AspectInstanceTest:

    def test_tastes(
            self, SubAspect, SubAspect_tastes, SubAspect_taste_values
    ):
        using_default_values = SubAspect('py')
        using_custom_values = SubAspect('py', **SubAspect_taste_values)
        assert using_default_values.tastes == {
            name: taste.default for name, taste in SubAspect_tastes.items()}
        assert using_custom_values.tastes == SubAspect_taste_values

    def test__setattr__(self, SubAspect, SubAspect_tastes):
        aspect = SubAspect('py')
        for name in SubAspect_tastes:
            with pytest.raises(AttributeError) as exc:
                setattr(aspect, name, 'value')
            assert str(exc.value) \
                == "can't set taste values of aspectclass instances"
        for name in ['docs', 'subaspects', 'tastes', '_tastes']:
            with pytest.raises(AttributeError) as exc:
                setattr(aspect, name, 'value')
            assert str(exc.value) \
                == "can't set attributes of aspectclass instances"
