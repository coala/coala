import os
import sys
import unittest

from coalib.misc.Shell import (prepare_string_argument,
                               escape_path_argument,
                               run_interactive_shell_command,
                               run_shell_command)


class EscapePathArgumentTest(unittest.TestCase):

    def test_escape_path_argument_linux_and_darwin(self):
        osnames = ("Linux", "Darwin")

        for osname in osnames:
            self.assertEqual(
                escape_path_argument("/home/usr/a-file", osname),
                "/home/usr/a-file")
            self.assertEqual(
                escape_path_argument("/home/usr/a-dir/", osname),
                "/home/usr/a-dir/")
            self.assertEqual(
                escape_path_argument("/home/us r/a-file with spaces.bla",
                                     osname),
                "/home/us\\ r/a-file\\ with\\ spaces.bla")
            self.assertEqual(
                escape_path_argument("/home/us r/a-dir with spaces/x/",
                                     osname),
                "/home/us\\ r/a-dir\\ with\\ spaces/x/")
            self.assertEqual(
                escape_path_argument(
                    "relative something/with cherries and/pickles.delicious",
                    osname),
                "relative\\ something/with\\ cherries\\ and/pickles.delicious")

    def test_escape_path_argument_windows(self):
        osname = "Windows"
        self.assertEqual(
            escape_path_argument("C:\\Windows\\has-a-weird-shell.txt", osname),
            "\"C:\\Windows\\has-a-weird-shell.txt\"")
        self.assertEqual(
            escape_path_argument("C:\\Windows\\lolrofl\\dirs\\", osname),
            "\"C:\\Windows\\lolrofl\\dirs\\\"")
        self.assertEqual(
            escape_path_argument("X:\\Users\\Maito Gai\\fi le.exe", osname),
            "\"X:\\Users\\Maito Gai\\fi le.exe\"")
        self.assertEqual(
            escape_path_argument("X:\\Users\\Mai to Gai\\director y\\",
                                 osname),
            "\"X:\\Users\\Mai to Gai\\director y\\\"")
        self.assertEqual(
            escape_path_argument("X:\\Users\\Maito Gai\\\"seven-gates\".y",
                                 osname),
            "\"X:\\Users\\Maito Gai\\^\"seven-gates^\".y\"")
        self.assertEqual(
            escape_path_argument("System32\\my-custom relative tool\\",
                                 osname),
            "\"System32\\my-custom relative tool\\\"")
        self.assertEqual(
            escape_path_argument("System32\\illegal\" name \"\".curd", osname),
            "\"System32\\illegal^\" name ^\"^\".curd\"")

    def test_escape_path_argument_unsupported_os(self):
        osname = "INVALID"
        self.assertEqual(
            escape_path_argument("/home/usr/a-file", osname),
            "/home/usr/a-file")
        self.assertEqual(
            escape_path_argument("/home/us r/a-file with spaces.bla", osname),
            "/home/us r/a-file with spaces.bla")
        self.assertEqual(
            escape_path_argument("|home|us r|a*dir with spaces|x|", osname),
            "|home|us r|a*dir with spaces|x|")
        self.assertEqual(
            escape_path_argument("system|a|b|c?d", osname),
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

    def test_prepare_string_argument_linux_and_darwin(self):
        testoses = ("Linux", "Darwin")
        expected_results = ('"normal_string"',
                            '"string with spaces"',
                            '"string with quotes\\"a"',
                            '"string with s-quotes\'b"',
                            '"bsn \n A"',
                            '"unrecognized \\q escape"')

        for string, result in zip(self.test_strings, expected_results):
            for testos in testoses:
                self.assertEqual(prepare_string_argument(string, testos),
                                 result)

    def test_prepare_string_argument_unsupported_os(self):
        testos = "WeIrD_O/S"

        for string in self.test_strings:
            self.assertEqual(prepare_string_argument(string, testos), string)


if __name__ == '__main__':
    unittest.main(verbosity=2)
