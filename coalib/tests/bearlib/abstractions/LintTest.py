import unittest

from coalib.bearlib.abstractions.Lint import Lint
from coalib.results.SourceRange import SourceRange
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.settings.Section import Section


class LintTest(unittest.TestCase):

    def test_process_output(self):
        section = Section("some_name")
        self.uut = Lint(section, None)
        out = list(self.uut.process_output(
            "1.0|0: Info message\n"
            "2.2|1: Normal message\n"
            "3.4|2: Major message\n",
            "a/file.py"))
        self.assertEqual(len(out), 3)
        self.assertEqual(out[0].origin, "Lint")

        self.assertEqual(out[0].affected_code[0],
                         SourceRange.from_values("a/file.py", 1, 0))
        self.assertEqual(out[0].severity, RESULT_SEVERITY.INFO)
        self.assertEqual(out[0].message, "Info message")

        self.assertEqual(out[1].affected_code[0],
                         SourceRange.from_values("a/file.py", 2, 2))
        self.assertEqual(out[1].severity, RESULT_SEVERITY.NORMAL)
        self.assertEqual(out[1].message, "Normal message")

        self.assertEqual(out[2].affected_code[0],
                         SourceRange.from_values("a/file.py", 3, 4))
        self.assertEqual(out[2].severity, RESULT_SEVERITY.MAJOR)
        self.assertEqual(out[2].message, "Major message")

        self.uut = Lint(section, None)
        self.uut.output_regex = (r'(?P<line>\d+)\.(?P<column>\d+)\|'
                                 r'(?P<end_line>\d+)\.(?P<end_column>\d+)\|'
                                 r'(?P<severity>\d+): (?P<message>.*)')
        self.uut.severity_map = {"I": RESULT_SEVERITY.INFO}
        out = list(self.uut.process_output(
            "1.0|2.3|0: Info message\n",
            'a/file.py'))
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0].affected_code[0].start.line, 1)
        self.assertEqual(out[0].affected_code[0].start.column, 0)
        self.assertEqual(out[0].affected_code[0].end.line, 2)
        self.assertEqual(out[0].affected_code[0].end.column, 3)
        self.assertEqual(out[0].severity, RESULT_SEVERITY.INFO)

        self.uut = Lint(section, None)
        out = list(self.uut.process_output(
            "Random line that shouldn't be captured\n"
            "*************\n",
            'a/file.py'))
        self.assertEqual(len(out), 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
