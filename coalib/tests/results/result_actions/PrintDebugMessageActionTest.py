import sys
import unittest

sys.path.insert(0, ".")
from coalib.results.result_actions.PrintDebugMessageAction import (
    PrintDebugMessageAction)
from coalib.misc.ContextManagers import retrieve_stdout
from coalib.settings.Section import Section
from coalib.results.Result import Result


class PrintDebugMessageActionTest(unittest.TestCase):
    def setUp(self):
        self.uut = PrintDebugMessageAction()
        self.test_result = Result("origin", "message", debug_msg="DEBUG MSG")

    def test_is_applicable(self):
        self.assertFalse(self.uut.is_applicable(1))
        self.assertFalse(self.uut.is_applicable(Result("o", "m")))
        self.assertTrue(self.uut.is_applicable(self.test_result))

    def test_apply(self):
        with retrieve_stdout() as stdout:
            self.uut.apply_from_section(self.test_result,
                                        {},
                                        {},
                                        Section("name"))
            self.assertEqual(stdout.getvalue(),
                             self.test_result.debug_msg+"\n")


if __name__ == '__main__':
    unittest.main(verbosity=2)
