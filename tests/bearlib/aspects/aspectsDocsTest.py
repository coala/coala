from coalib.bearlib.aspects import Root
from coalib.bearlib.aspects.docs import Documentation


class aspectsDocsTest:

    def test_aspects_docs(self):

        def check(aspects):
            for aspect in aspects:
                assert isinstance(aspect.docs, Documentation)
                assert aspect.docs.check_consistency()
                check(aspect.subaspects.values())

        check(Root.subaspects.values())
