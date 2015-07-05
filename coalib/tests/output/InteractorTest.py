import unittest
import sys
import builtins
import shutil

sys.path.insert(0, ".")
from coalib.output.Interactor import Interactor
from coalib.output.printers.ConsolePrinter import ConsolePrinter
from coalib.results.Result import Result
from coalib.results.Diff import Diff


class InteractorTest(unittest.TestCase):
    def setUp(self):
        self.uut = Interactor(ConsolePrinter())

    def test_api(self):
        self.assertRaises(NotImplementedError,
                          self.uut.acquire_settings,
                          "anything")
        self.assertRaises(NotImplementedError,
                          self.uut.print_result,
                          Result("message", "origin"), {})
        self.assertRaises(NotImplementedError,
                          self.uut.print_result,
                          Result("origin",
                                 "line",
                                 "message",
                                 "file",
                                 line_nr=1),
                          {})
        self.assertRaises(NotImplementedError, self.uut.begin_section, "name")
        self.assertRaises(NotImplementedError, self.uut.show_bears, {})
        self.assertRaises(NotImplementedError, self.uut.did_nothing)
        self.assertRaises(TypeError, self.uut.print_results, 5, {})
        self.assertRaises(TypeError, self.uut.print_results, [], 5)
        self.assertRaises(NotImplementedError,
                          self.uut.print_results,
                          [Result("message", "origin")], {})
        self.assertRaises(NotImplementedError, self.uut._print_actions, 5)
        self.assertRaises(NotImplementedError,
                          self.uut._print_action_failed,
                          "t",
                          Exception())

        self.uut.print_results([], {})
        self.uut.print_results(["illegal value"], {})

        self.assertEqual(self.uut.get_metadata().non_optional_params, {})
        self.assertEqual(self.uut.get_metadata().optional_params, {})

    def test_finalize_failse(self):
        def raise_error(file, mode=""):
            raise Exception

        _open = builtins.__dict__["open"]
        try:
            builtins.__dict__["open"] = raise_error
            shutil.copy2 = lambda src, dst: self.assertEqual(src+".orig", dst)

            diff = Diff()
            diff.delete_line(2)

            self.uut.file_diff_dict = {"f": diff}
            # Should catch any exception during write back
            self.uut.finalize({"f": ["1", "2", "3"]})
        finally:
            builtins.__dict__["open"] = _open


if __name__ == '__main__':
    unittest.main(verbosity=2)
