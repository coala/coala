from types import ModuleType

import coalib.bearlib.aspects
from coalib.bearlib.aspects.exceptions import (AspectNotFoundError,
                                               MultipleAspectFoundError)

import pytest
import unittest


class aspectsModuleTest(unittest.TestCase):

    def test_module(self):
        # check that module is correctly wrapped
        assert isinstance(coalib.bearlib.aspects, ModuleType)
        assert type(coalib.bearlib.aspects) is not ModuleType
        assert (type(coalib.bearlib.aspects) is
                coalib.bearlib.aspects.aspectsModule)

    def test__getitem__(self):
        dict_spelling = coalib.bearlib.aspects.Root.Spelling.DictionarySpelling
        # check a leaf aspect
        for aspectname in ['DictionarySpelling',
                           'spelling.DictionarySpelling',
                           'root.SPELLING.DictionarySpelling']:
            assert coalib.bearlib.aspects[aspectname] is dict_spelling
        # check a container aspect
        for aspectname in ['Spelling', 'SPELLING', 'ROOT.spelling']:
            assert (coalib.bearlib.aspects[aspectname] is
                    coalib.bearlib.aspects.Root.Spelling)
        # check root aspect
        for aspectname in ['Root', 'root', 'ROOT']:
            assert (coalib.bearlib.aspects[aspectname] is
                    coalib.bearlib.aspects.Root)

    def test__getitem__no_match(self):
        for aspectname in ['noaspect', 'NOASPECT',
                           'Root.DictionarySpelling']:
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

    def test_get(self):
        # check a leaf aspect
        for aspectname in ['clone', 'redundancy.clone',
                           'root.redundancy.clone']:
            self.assertIs(coalib.bearlib.aspects.get(aspectname),
                          coalib.bearlib.aspects.Root.Redundancy.Clone)
        # check a container aspect
        for aspectname in ['Spelling', 'SPELLING', 'ROOT.spelling']:
            self.assertIs(coalib.bearlib.aspects.get(aspectname),
                          coalib.bearlib.aspects.Root.Spelling)
        # check root aspect
        for aspectname in ['Root', 'root', 'ROOT']:
            self.assertIs(coalib.bearlib.aspects.get(aspectname),
                          coalib.bearlib.aspects.Root)

    def test_get_no_match(self):
        for aspectname in ['noaspect', 'NOASPECT', 'Root.aspectsYEAH']:
            self.assertIsNone(coalib.bearlib.aspects.get(aspectname))

    def test_get_multi_match(self):
        with self.assertRaisesRegex(
                MultipleAspectFoundError,
                r"^Multiple aspects named 'length'. "
                r'Choose from '
                r'\[<aspectclass'
                r" 'Root.Metadata.CommitMessage.Body.Length'>,"
                r' <aspectclass'
                r" 'Root.Metadata.CommitMessage.Shortlog.Length'>"
                r'\]$'):
            coalib.bearlib.aspects.get('length')
