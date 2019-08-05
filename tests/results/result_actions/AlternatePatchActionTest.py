import unittest
from coalib.results.Result import Result
from coalib.results.Diff import Diff
from coalib.settings.Section import Section, Setting
from coalib.results.result_actions.AlternatePatchAction import (
    AlternatePatchAction)
from coala_utils.ContextManagers import retrieve_stdout


class AlternatePatchActionTest(unittest.TestCase):

    def setUp(self):
        diff0 = Diff(['coler'])
        diff0.modify_line(1, 'color')

        diff1 = Diff(['coler'])
        diff1.modify_line(1, 'colour')

        diff2 = Diff(['coler'])
        diff2.modify_line(1, 'cooler')

        diff3 = Diff(['coler'])
        diff3.modify_line(1, 'coder')

        self.original_diff = {'filename': diff0}
        self.alternate_diff1 = {'filename': diff1}
        self.alternate_diff2 = {'filename': diff2}
        self.alternate_diff3 = {'filename': diff3}
        self.alternate_diffs = [self.alternate_diff1,
                                self.alternate_diff2,
                                self.alternate_diff3]
        self.result = Result('origin', 'message',
                             diffs=self.original_diff,
                             alternate_diffs=self.alternate_diffs)
        self.original_file_dict = {'filename': ['coler']}
        self.section = Section('name')
        self.section.append(Setting('no_color', 'True'))

        self.uut1 = AlternatePatchAction(self.alternate_diff1, 1)
        self.uut2 = AlternatePatchAction(self.alternate_diff2, 2)
        self.uut3 = AlternatePatchAction(self.alternate_diff3, 3)

    def test_is_applicable(self):
        retval = self.uut1.is_applicable(self.result,
                                         self.original_file_dict, {},
                                         applied_actions=('ShowPatchAction'))
        self.assertTrue(retval)

        retval = self.uut1.is_applicable(self.result,
                                         self.original_file_dict, {},
                                         applied_actions=('ShowPatchAction',
                                                          'ApplyPatchAction'))
        self.assertFalse(retval)

    def test_apply(self):
        self.assertEqual(self.uut1.description, 'Show Alternate Patch 1')
        self.assertEqual(self.uut2.description, 'Show Alternate Patch 2')
        self.assertEqual(self.uut3.description, 'Show Alternate Patch 3')

        with retrieve_stdout() as stdout:
            self.uut1.apply_from_section(self.result,
                                         self.original_file_dict,
                                         {}, self.section)
            self.assertEqual(stdout.getvalue(),
                             '[----] filename\n'
                             '[++++] filename\n'
                             '[   1] coler\n'
                             '[   1] colour\n')
            self.uut1.diffs = self.original_diff
            self.result.diffs = self.alternate_diff1

        self.assertEqual(self.uut1.description, 'Show Original Patch')
        self.assertEqual(self.uut2.description, 'Show Alternate Patch 2')
        self.assertEqual(self.uut3.description, 'Show Alternate Patch 3')

        with retrieve_stdout() as stdout:
            self.uut2.apply_from_section(self.result,
                                         self.original_file_dict,
                                         {}, self.section)
            self.assertEqual(stdout.getvalue(),
                             '[----] filename\n'
                             '[++++] filename\n'
                             '[   1] coler\n'
                             '[   1] cooler\n')
            self.uut2.diffs = self.alternate_diff1
            self.result.diffs = self.alternate_diff2

        self.assertEqual(self.uut1.description, 'Show Original Patch')
        self.assertEqual(self.uut2.description, 'Show Alternate Patch 1')
        self.assertEqual(self.uut3.description, 'Show Alternate Patch 3')

        with retrieve_stdout() as stdout:
            self.uut3.apply_from_section(self.result,
                                         self.original_file_dict,
                                         {}, self.section)
            self.assertEqual(stdout.getvalue(),
                             '[----] filename\n'
                             '[++++] filename\n'
                             '[   1] coler\n'
                             '[   1] coder\n')
            self.uut3.diffs = self.alternate_diff2
            self.result.diffs = self.alternate_diff3

        self.assertEqual(self.uut1.description, 'Show Original Patch')
        self.assertEqual(self.uut2.description, 'Show Alternate Patch 1')
        self.assertEqual(self.uut3.description, 'Show Alternate Patch 2')

        with retrieve_stdout() as stdout:
            self.uut3.apply_from_section(self.result,
                                         self.original_file_dict,
                                         {}, self.section)
            self.assertEqual(stdout.getvalue(),
                             '[----] filename\n'
                             '[++++] filename\n'
                             '[   1] coler\n'
                             '[   1] cooler\n')
            self.uut3.diffs = self.alternate_diff3
            self.result.diffs = self.alternate_diff2

        self.assertEqual(self.uut1.description, 'Show Original Patch')
        self.assertEqual(self.uut2.description, 'Show Alternate Patch 1')
        self.assertEqual(self.uut3.description, 'Show Alternate Patch 3')

        with retrieve_stdout() as stdout:
            self.uut2.apply_from_section(self.result,
                                         self.original_file_dict,
                                         {}, self.section)
            self.assertEqual(stdout.getvalue(),
                             '[----] filename\n'
                             '[++++] filename\n'
                             '[   1] coler\n'
                             '[   1] colour\n')
            self.uut2.diffs = self.alternate_diff2
            self.result.diffs = self.alternate_diff1

        self.assertEqual(self.uut1.description, 'Show Original Patch')
        self.assertEqual(self.uut2.description, 'Show Alternate Patch 2')
        self.assertEqual(self.uut3.description, 'Show Alternate Patch 3')

        with retrieve_stdout() as stdout:
            self.uut1.apply_from_section(self.result,
                                         self.original_file_dict,
                                         {}, self.section)
            self.assertEqual(stdout.getvalue(),
                             '[----] filename\n'
                             '[++++] filename\n'
                             '[   1] coler\n'
                             '[   1] color\n')
            self.uut1.diffs = self.alternate_diff1
            self.result.diffs = self.original_diff

        self.assertEqual(self.uut1.description, 'Show Alternate Patch 1')
        self.assertEqual(self.uut2.description, 'Show Alternate Patch 2')
        self.assertEqual(self.uut3.description, 'Show Alternate Patch 3')

    def test_update_description(self):
        result = self.result
        result.diffs, self.uut2.diffs = self.uut2.diffs, result.diffs

        self.uut2.update_description(result)
        self.assertEqual(self.uut2.description, 'Show Original Patch')

        result.diffs, self.uut2.diffs = self.uut2.diffs, result.diffs
        self.uut2.update_description(result)
        self.assertEqual(self.uut2.description, 'Show Alternate Patch 2')
