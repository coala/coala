import os
import sys
import unittest

from coalib.misc.Shell import (
    escape_path_argument, prepare_string_argument,
    run_interactive_shell_command, run_shell_command)


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
            "/home/us\\ r/a-file\\ with\\ spaces.bla")
        self.assertEqual(
            escape_path_argument("/home/us r/a-dir with spaces/x/",
                                 _type),
            "/home/us\\ r/a-dir\\ with\\ spaces/x/")
        self.assertEqual(
            escape_path_argument(
                "relative something/with cherries and/pickles.delicious",
                _type),
            "relative\\ something/with\\ cherries\\ and/pickles.delicious")

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


class RunShellCommandTest(unittest.TestCase):

    @staticmethod
    def construct_testscript_command(scriptname):
        return " ".join(
            escape_path_argument(s) for s in (
                sys.executable,
                os.path.join(os.path.dirname(os.path.realpath(__file__)),
                             "run_shell_command_testfiles",
                             scriptname)))

    def test_run_interactive_shell_command(self):
        command = RunShellCommandTest.construct_testscript_command(
            "test_interactive_program.py")

        with run_interactive_shell_command(command) as p:
            self.assertEqual(p.stdout.readline(), "test_program X\n")
            self.assertEqual(p.stdout.readline(), "Type in a number:\n")
            p.stdin.write("33\n")
            p.stdin.flush()
            self.assertEqual(p.stdout.readline(), "33\n")
            self.assertEqual(p.stdout.readline(), "Exiting program.\n")

    def test_run_interactive_shell_command_kwargs_delegation(self):
        with self.assertRaises(TypeError):
            with run_interactive_shell_command("some_command",
                                               weird_parameter=30):
                pass

        # Test one of the forbidden parameters.
        with self.assertRaises(TypeError):
            with run_interactive_shell_command("some_command", shell=False):
                pass

    def test_run_shell_command_without_stdin(self):
        command = RunShellCommandTest.construct_testscript_command(
            "test_program.py")

        stdout, stderr = run_shell_command(command)

        expected = ("test_program Z\n"
                    "non-interactive mode.\n"
                    "Exiting...\n")
        self.assertEqual(stdout, expected)
        self.assertEqual(stderr, "")

    def test_run_shell_command_with_stdin(self):
        command = RunShellCommandTest.construct_testscript_command(
            "test_input_program.py")

        stdout, stderr = run_shell_command(command, "1  4  10  22")

        self.assertEqual(stdout, "37\n")
        self.assertEqual(stderr, "")

        stdout, stderr = run_shell_command(command, "1 p 5")

        self.assertEqual(stdout, "")
        self.assertEqual(stderr, "INVALID INPUT\n")

    def test_run_shell_command_kwargs_delegation(self):
        with self.assertRaises(TypeError):
            run_shell_command("super-cool-command", weird_parameter2="abc")

        # Test one of the forbidden parameters.
        with self.assertRaises(TypeError):
            run_shell_command("super-cool-command", universal_newlines=False)


class PrepareStringArgumentTest(unittest.TestCase):

    def setUp(self):
        self.test_strings = ("normal_string",
                             "string with spaces",
                             'string with quotes"a',
                             "string with s-quotes'b",
                             "bsn \n A",
                             "unrecognized \\q escape")

    def test_prepare_string_argument_sh(self):
        expected_results = ('"normal_string"',
                            '"string with spaces"',
                            '"string with quotes\\"a"',
                            '"string with s-quotes\'b"',
                            '"bsn \n A"',
                            '"unrecognized \\q escape"')

        for string, result in zip(self.test_strings, expected_results):
            self.assertEqual(prepare_string_argument(string, "sh"),
                             result)

    def test_prepare_string_argument_unsupported(self):
        for string in self.test_strings:
            self.assertEqual(prepare_string_argument(string, "WeIrD_O/S"),
                             string)
