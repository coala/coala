from coalib.bearlib.aspects import aspectclass

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
