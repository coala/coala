import unittest

from coala_utils.ContextManagers import retrieve_stdout
from coalib.results.Result import Result
from coalib.results.result_actions.PrintAspectAction import PrintAspectAction
from coalib.settings.Section import Section
from coalib.bearlib.aspects import Root


class PrintAspectActionTest(unittest.TestCase):

    def setUp(self):
        self.uut = PrintAspectAction()

        @Root.subaspect
        class test_aspect:
            """
            This is a test aspect
            """
            class docs:
                example = 'test'
                example_language = 'test'
                importance_reason = 'test'
                fix_suggestions = 'test'

        self.test_aspect = test_aspect('py')
        self.test_result = Result('origin', 'message', aspect=self.test_aspect)

    def test_is_applicable(self):
        with self.assertRaises(TypeError):
            self.uut.is_applicable(1, None, None)

        self.assertEqual(
            'There is no aspect associated with the result.',
            self.uut.is_applicable(Result('o', 'm'), None, None))

        self.assertTrue(self.uut.is_applicable(self.test_result, None, None))

    def test_apply(self):
        with retrieve_stdout() as stdout:
            self.assertEqual(self.uut.apply_from_section(self.test_result,
                                                         {},
                                                         {},
                                                         Section('name')),
                             {})
            self.assertEqual(stdout.getvalue(),
                             type(self.test_aspect).__qualname__ + '\n' +
                             type(self.test_aspect).docs.definition + '\n')
