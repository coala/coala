import unittest

from coala_utils.ContextManagers import retrieve_stdout
from coalib.results.Result import Result
from coalib.results.result_actions.PrintAspectAction import PrintAspectAction
from coalib.settings.Section import Section
from coalib.bearlib.aspects import Root


class PrintAspectActionTest(unittest.TestCase):

    def setUp(self):
        self.utt = PrintAspectAction()
        self.test_result = Result('origin', 'message', aspect=Root)

    def test_is_applicable(self):
        self.assertFalse(self.uut.is_applicable(1, None, None))
        self.assertFalse(self.uut.is_applicable(Result('o', 'm'), None, None))
        self.assertTrue(self.uut.is_applicable(self.test_result, None, None))

    def test_apply(self):
        with retrieve_stdout() as stdout:
            self.assertEqual(self.uut.apply_from_section(self.test_result,
                                                         {},
                                                         {},
                                                         Section('name')),
                             {})
            self.assertEqual(stdout.getvalue(),
                             self.test_result.aspect+'\n')
