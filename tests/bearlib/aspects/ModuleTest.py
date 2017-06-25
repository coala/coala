from types import ModuleType

import coalib.bearlib.aspects
from coalib.bearlib.aspects.exceptions import (AspectNotFoundError,
                                               MultipleAspectFoundError)

import pytest


class aspectsModuleTest:

    def test_module(self):
        # check that module is correctly wrapped
        assert isinstance(coalib.bearlib.aspects, ModuleType)
        assert type(coalib.bearlib.aspects) is not ModuleType
        assert (type(coalib.bearlib.aspects) is
                coalib.bearlib.aspects.aspectsModule)

    def test__getitem__(self):
        # check a leaf aspect
        for aspectname in ['aspectsYEAH', 'spelling.aspectsYEAH',
                           'root.SPELLING.aspectsYEAH']:
            assert (coalib.bearlib.aspects[aspectname] is
                    coalib.bearlib.aspects.Root.Spelling.aspectsYEAH)
        # check a container aspect
        for aspectname in ['Spelling', 'SPELLING', 'ROOT.spelling']:
            assert (coalib.bearlib.aspects[aspectname] is
                    coalib.bearlib.aspects.Root.Spelling)
        # check root aspect
        for aspectname in ['Root', 'root', 'ROOT']:
            assert (coalib.bearlib.aspects[aspectname] is
                    coalib.bearlib.aspects.Root)

    def test__getitem__no_match(self):
        for aspectname in ['noaspect', 'NOASPECT', 'Root.aspectsYEAH']:
            with pytest.raises(AspectNotFoundError) as exc:
                coalib.bearlib.aspects[aspectname]
            exc.match(r"^No aspect named '%s'$" % aspectname)

    def test__getitem__multi_match(self):
        for aspectname in ['Length', 'length', 'LENGTH']:
            with pytest.raises(MultipleAspectFoundError) as exc:
                coalib.bearlib.aspects[aspectname]
            exc.match(r"^Multiple aspects named '%s'. " % aspectname +
                      r'Choose from '
                      r'\[<aspectclass'
                      r" 'Root.Metadata.CommitMessage.Body.Length'>,"
                      r' <aspectclass'
                      r" 'Root.Metadata.CommitMessage.Shortlog.Length'>"
                      r'\]$')
