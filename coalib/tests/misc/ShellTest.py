import sys
import unittest

sys.path.insert(0, ".")
from coalib.misc.Shell import escape_path_argument


class ShellTest(unittest.TestCase):
    # Tests the function that makes a path shell-argument-ready.

    def test_escape_path_argument(self):
        osname = "Linux"
        self.assertEqual(
            escape_path_argument("/home/usr/a-file", osname),
            "/home/usr/a-file")
        self.assertEqual(
            escape_path_argument("/home/usr/a-dir/", osname),
            "/home/usr/a-dir/")
        self.assertEqual(
            escape_path_argument("/home/us r/a-file with spaces.bla", osname),
            "/home/us\\ r/a-file\\ with\\ spaces.bla")
        self.assertEqual(
            escape_path_argument("/home/us r/a-dir with spaces/x/", osname),
            "/home/us\\ r/a-dir\\ with\\ spaces/x/")
        self.assertEqual(
            escape_path_argument(
                "relative something/with cherries and/pickles.delicious",
                osname),
            "relative\\ something/with\\ cherries\\ and/pickles.delicious")

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


if __name__ == '__main__':
    unittest.main(verbosity=2)
