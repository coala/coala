import unittest

from bears.tests.BearTestHelper import generate_skip_decorator
from bears.c_languages.IndentBear import IndentBear
from coalib.bearlib.abstractions.Lint import Lint
from coalib.results.SourceRange import SourceRange
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.settings.Section import Section


class LintTest(unittest.TestCase):

    def setUp(self):
        section = Section("some_name")
        self.uut = Lint(section, None)

    def test_invalid_output(self):
        out = list(self.uut.process_output(
            ["1.0|0: Info message\n",
             "2.2|1: Normal message\n",
             "3.4|2: Major message\n"],
            "a/file.py",
            ['original_file_lines_placeholder']))
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

    def test_custom_regex(self):
        self.uut.output_regex = (r'(?P<origin>\w+)\|'
                                 r'(?P<line>\d+)\.(?P<column>\d+)\|'
                                 r'(?P<end_line>\d+)\.(?P<end_column>\d+)\|'
                                 r'(?P<severity>\d+): (?P<message>.*)')
        self.uut.severity_map = {"I": RESULT_SEVERITY.INFO}
        out = list(self.uut.process_output(
            ["info_msg|1.0|2.3|0: Info message\n"],
            'a/file.py',
            ['original_file_lines_placeholder']))
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0].affected_code[0].start.line, 1)
        self.assertEqual(out[0].affected_code[0].start.column, 0)
        self.assertEqual(out[0].affected_code[0].end.line, 2)
        self.assertEqual(out[0].affected_code[0].end.column, 3)
        self.assertEqual(out[0].severity, RESULT_SEVERITY.INFO)
        self.assertEqual(out[0].origin, 'Lint (info_msg)')

    def test_valid_output(self):
        out = list(self.uut.process_output(
            ["Random line that shouldn't be captured\n",
             "*************\n"],
            'a/file.py',
            ['original_file_lines_placeholder']))
        self.assertEqual(len(out), 0)

    @generate_skip_decorator(IndentBear)
    def test_stdin_input(self):
        self.uut.executable = IndentBear.executable
        self.uut.use_stdin = True
        self.uut.use_stderr = False
        self.uut.process_output = lambda output, filename, file: output

        input_file = ["int main(){return 0;}"]
        out = self.uut.lint(file=input_file)
        self.assertEqual(out,
                         ['int\n', 'main ()\n', '{\n', '  return 0;\n', '}\n'])

    def test_missing_binary(self):
        old_binary = Lint.executable
        invalid_binary = "invalid_binary_which_doesnt_exist"
        Lint.executable = invalid_binary

        self.assertEqual(Lint.check_prerequisites(),
                         "'{}' is not installed.".format(invalid_binary))

        # "echo" is existent on nearly all platforms.
        Lint.executable = "echo"
        self.assertTrue(Lint.check_prerequisites())

        del Lint.executable
        self.assertTrue(Lint.check_prerequisites())

        Lint.executable = old_binary

    def test_config_file_generator(self):
        self.uut.executable = "echo"
        self.uut.arguments = "-c {config_file}"

        self.assertEqual(
            self.uut._create_command(config_file="configfile").strip(),
            "echo -c configfile")
