from coalib.bearlib.aspects import Root
from coalib.bearlib.aspects.meta import issubaspect

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
        with pytest.raises(TypeError) as exc:
            issubaspect('String', SubAspect)
        assert (str(exc.value) == "'String' is not an aspectclass or "
                'an instance of an aspectclass')
        with pytest.raises(TypeError) as exc:
            issubaspect(RootAspect, str)
        assert (str(exc.value) == "<class 'str'> is not an aspectclass or "
                'an instance of an aspectclass')
        assert issubaspect(SubAspect('Python'), RootAspect)
