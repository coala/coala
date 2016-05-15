import os
import unittest

from coalib.bearlib.abstractions.Lint import Lint, escape_path_argument
from coalib.misc.ContextManagers import prepare_file
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.results.SourceRange import SourceRange
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
                                 r'(?P<severity>\w+): (?P<message>.*)')
        self.uut.severity_map = {"I": RESULT_SEVERITY.INFO}
        out = list(self.uut.process_output(
            ["info_msg|1.0|2.3|I: Info message\n"],
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

    def test_stdin_input(self):
        with prepare_file(["abcd", "efgh"], None) as (lines, filename):
            # Use more which is a command that can take stdin and show it.
            # This is available in windows and unix.
            self.uut.executable = "more"
            self.uut.use_stdin = True
            self.uut.use_stderr = False
            self.uut.process_output = lambda output, filename, file: output

            out = self.uut.lint(file=lines)
            # Some implementations of `more` add an extra newline at the end.
            self.assertTrue(("abcd\n", "efgh\n") == out or
                            ("abcd\n", "efgh\n", "\n") == out)

    def test_stderr_output(self):
        self.uut.executable = "echo"
        self.uut.arguments = "hello"
        self.uut.use_stdin = False
        self.uut.use_stderr = True
        self.uut.process_output = lambda output, filename, file: output
        out = self.uut.lint("unused_filename")
        self.assertEqual((), out)  # stderr is used

        self.uut.use_stderr = False
        out = self.uut.lint("unused_filename")
        self.assertEqual(('hello\n',), out)  # stdout is used

        def assert_warn(line):
            assert line == "hello"
        old_warn = self.uut.warn
        self.uut.warn = assert_warn
        self.uut._print_errors(["hello", "\n"])
        self.uut.warn = old_warn

    def test_gives_corrected(self):
        self.uut.gives_corrected = True
        out = tuple(self.uut.process_output(["a", "b"], "filename", ["a", "b"]))
        self.assertEqual((), out)
        out = tuple(self.uut.process_output(["a", "b"], "filename", ["a"]))
        self.assertEqual(len(out), 1)

    def test_check_prerequisites(self):
        old_binary = Lint.executable
        invalid_binary = "invalid_binary_which_doesnt_exist"
        Lint.executable = invalid_binary

        self.assertEqual(Lint.check_prerequisites(),
                         "'{}' is not installed.".format(invalid_binary))

        # "echo" is existent on nearly all platforms.
        Lint.executable = "echo"
        self.assertTrue(Lint.check_prerequisites())

        Lint.executable = old_binary

        old_command = Lint.prerequisite_command

        Lint.prerequisite_command = ["command_which_doesnt_exist"]
        self.assertEqual(Lint.check_prerequisites(), Lint.prerequisite_fail_msg)

        Lint.prerequisite_command = "command_which_isnt_a_list"
        self.assertRaises(TypeError, Lint.check_prerequisites)

        Lint.prerequisite_command = ["cd",
                                     os.path.join('non', 'existent', 'path')]
        self.assertEqual(Lint.check_prerequisites(), Lint.prerequisite_fail_msg)

        Lint.prerequisite_command = ["echo", "abc"]
        self.assertTrue(Lint.check_prerequisites())

        Lint.prerequisite_command = old_command

    def test_config_file_generator(self):
        self.uut.executable = "echo"
        self.uut.arguments = "-c {config_file}"

        self.assertEqual(
            self.uut._create_command(config_file="configfile").strip(),
            "echo -c " + escape_path_argument("configfile"))

    def test_generate_config_file_generator(self):
        self.uut.executable = "echo"
        self.uut.config_file = lambda: ["config line1"]
        config_filename = self.uut.generate_config_file()
        self.assertTrue(os.path.isfile(config_filename))
        os.remove(config_filename)

        # To complete coverage of closing the config file and check if any
        # errors are thrown there.
        self.uut.lint("filename")


class EscapePathArgumentTest(unittest.TestCase):

    def test_escape_path_argument_sh(self):
        _type = "sh"
        self.assertEqual(
            escape_path_argument("/home/usr/a-file", _type),
            "/home/usr/a-file")
        self.assertEqual(
            escape_path_argument("/home/usr/a-dir/", _type),
            "/home/usr/a-dir/")
        self.assertEqual(
            escape_path_argument("/home/us r/a-file with spaces.bla",
                                 _type),
            "'/home/us r/a-file with spaces.bla'")
        self.assertEqual(
            escape_path_argument("/home/us r/a-dir with spaces/x/",
                                 _type),
            "'/home/us r/a-dir with spaces/x/'")
        self.assertEqual(
            escape_path_argument(
                "relative something/with cherries and/pickles.delicious",
                _type),
            "'relative something/with cherries and/pickles.delicious'")

    def test_escape_path_argument_cmd(self):
        _type = "cmd"
        self.assertEqual(
            escape_path_argument("C:\\Windows\\has-a-weird-shell.txt", _type),
            "\"C:\\Windows\\has-a-weird-shell.txt\"")
        self.assertEqual(
            escape_path_argument("C:\\Windows\\lolrofl\\dirs\\", _type),
            "\"C:\\Windows\\lolrofl\\dirs\\\"")
        self.assertEqual(
            escape_path_argument("X:\\Users\\Maito Gai\\fi le.exe", _type),
            "\"X:\\Users\\Maito Gai\\fi le.exe\"")
        self.assertEqual(
            escape_path_argument("X:\\Users\\Mai to Gai\\director y\\",
                                 _type),
            "\"X:\\Users\\Mai to Gai\\director y\\\"")
        self.assertEqual(
            escape_path_argument("X:\\Users\\Maito Gai\\\"seven-gates\".y",
                                 _type),
            "\"X:\\Users\\Maito Gai\\^\"seven-gates^\".y\"")
        self.assertEqual(
            escape_path_argument("System32\\my-custom relative tool\\",
                                 _type),
            "\"System32\\my-custom relative tool\\\"")
        self.assertEqual(
            escape_path_argument("System32\\illegal\" name \"\".curd", _type),
            "\"System32\\illegal^\" name ^\"^\".curd\"")

    def test_escape_path_argument_unsupported(self):
        _type = "INVALID"
        self.assertEqual(
            escape_path_argument("/home/usr/a-file", _type),
            "/home/usr/a-file")
        self.assertEqual(
            escape_path_argument("/home/us r/a-file with spaces.bla", _type),
            "/home/us r/a-file with spaces.bla")
        self.assertEqual(
            escape_path_argument("|home|us r|a*dir with spaces|x|", _type),
            "|home|us r|a*dir with spaces|x|")
        self.assertEqual(
            escape_path_argument("system|a|b|c?d", _type),
            "system|a|b|c?d")
