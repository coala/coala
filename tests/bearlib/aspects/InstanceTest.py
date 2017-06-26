import pytest

import coalib.bearlib.aspects


class AspectInstanceTest:

    def test_tastes(
            self, SubAspect, SubAspect_tastes, SubAspect_taste_values):
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
                == "A 'taste' value for this aspectclass instance "\
                   'exists already.'
        for name in ['docs', 'subaspects', 'tastes', '_tastes']:
            with pytest.raises(AttributeError) as exc:
                setattr(aspect, name, 'value')
            assert str(exc.value) \
                == "can't set attributes of aspectclass instances"

    def test_get(self, RootAspect, SubAspect, SubSubAspect):
        assert RootAspect.get(RootAspect) is RootAspect
        assert RootAspect.get(SubAspect) is SubAspect
        assert RootAspect.get(SubSubAspect) is SubSubAspect
        assert SubAspect.get(SubSubAspect) is SubSubAspect

        metadata = coalib.bearlib.aspects.Metadata
        assert metadata.get('commitmessage') is metadata.CommitMessage
        assert metadata.get('body') is metadata.CommitMessage.Body

        assert SubAspect.get(RootAspect) is None

        with pytest.raises(NotImplementedError) as exc:
            RootAspect('py').get(SubAspect)
        exc.match('Cannot access children of aspect instance.')

        with pytest.raises(AttributeError) as exc:
            RootAspect.get(SubAspect('py'))
        exc.match('Cannot search an aspect instance using '
                  'another aspect instance as argument.')

        with pytest.raises(AttributeError) as exc:
            RootAspect('py').get(SubAspect('py'))
        exc.match('Cannot search an aspect instance using '
                  'another aspect instance as argument.')
