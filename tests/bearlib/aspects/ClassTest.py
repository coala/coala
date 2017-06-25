from coalib.bearlib.aspects import Root, AspectTypeError as aspectTypeError
from coalib.bearlib.aspects.meta import isaspect, assert_aspect, issubaspect

import pytest


class AspectClassTest:

    def test_subaspect_without_definition(self, RootAspect):
        with pytest.raises(TypeError):
            @RootAspect.subaspect
            class SubAspect:
                pass

    def test_subaspect_without_docs(self, RootAspect):
        @RootAspect.subaspect
        class SubAspect:
            """
            Definition
            """

        assert not SubAspect.docs.check_consistency()

    def test_subaspect_without_enough_docs(self, RootAspect):
        @RootAspect.subaspect
        class SubAspect:
            """
            Description
            """

            class docs:
                example = 'Example'

        assert not SubAspect.docs.check_consistency()


class IsaspectFunctionTest:

    def test_isaspect(self, RootAspect):
        @RootAspect.subaspect
        class SubAspect:
            """
            Description
            """

        assert isaspect(RootAspect)
        assert isaspect(SubAspect)
        assert isaspect(SubAspect('Python'))
        assert isaspect(Root('py'))
        assert not isaspect('String')


class Assert_aspectFunctionTest:

    def test_assert_aspect(self, RootAspect):
        @RootAspect.subaspect
        class SubAspect:
            """
            Description
            """

        assert assert_aspect(RootAspect) == RootAspect
        assert assert_aspect(SubAspect) == SubAspect
        assert assert_aspect(Root) == Root
        with pytest.raises(aspectTypeError) as exc:
            assert_aspect('String')
        assert (str(exc.value) == "'String' is not an aspectclass or "
                'an instance of an aspectclass')


class IssubaspectFunctionTest:

    def test_issubaspect(self, RootAspect):
        @RootAspect.subaspect
        class SubAspect:
            """
            Description
            """

        assert issubaspect(SubAspect, RootAspect)
        assert not issubaspect(Root, RootAspect)
        assert issubaspect(RootAspect, RootAspect)
        with pytest.raises(aspectTypeError) as exc:
            issubaspect('String', SubAspect)
        assert not isaspect('String')
        assert (str(exc.value) == "'String' is not an aspectclass or "
                'an instance of an aspectclass')
        with pytest.raises(aspectTypeError) as exc:
            issubaspect(RootAspect, str)
        assert not isaspect(str)
        assert (str(exc.value) == "<class 'str'> is not an aspectclass or "
                'an instance of an aspectclass')
        assert issubaspect(SubAspect('Python'), RootAspect)
