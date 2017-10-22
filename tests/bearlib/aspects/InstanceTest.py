import pytest

import coalib.bearlib.aspects
import coalib.bearlib.aspects.Metadata as Metadata


class AspectInstanceTest:

    def test_instantiation(self, RootAspect, SubAspect, SubSubAspect):
        root_instance = RootAspect('py')
        instance_counter = 0

        def test_child(aspects):
            for aspect in aspects:
                assert isinstance(aspect, coalib.bearlib.aspects.aspectbase)
                nonlocal instance_counter
                instance_counter += 1
                if aspect.subaspects:
                    test_child(aspect.subaspects.values())
        test_child([root_instance])
        # RootAspect itself + 2 of its recursive subaspects
        assert instance_counter == 3

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

        assert RootAspect('py').get(SubAspect) == SubAspect('py')
        assert RootAspect('py').get(SubSubAspect) == SubSubAspect('py')

        with pytest.raises(AttributeError) as exc:
            RootAspect.get(SubAspect('py'))
        exc.match('Cannot search an aspect instance using '
                  'another aspect instance as argument.')

        with pytest.raises(AttributeError) as exc:
            RootAspect('py').get(SubAspect('py'))
        exc.match('Cannot search an aspect instance using '
                  'another aspect instance as argument.')

    def test_get_leaf_aspects(self, RootAspect, SubAspect, SubSubAspect):
        assert RootAspect.get_leaf_aspects() == [SubSubAspect]
        assert RootAspect('py').get_leaf_aspects() == [SubSubAspect('py')]

        assert (Metadata.get_leaf_aspects() ==
                Metadata.CommitMessage.get_leaf_aspects())
