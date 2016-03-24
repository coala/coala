import json
import unittest
from unittest.case import SkipTest

from coalib.output.JSONEncoder import create_json_encoder
from coalib.results.Diff import ConflictError, Diff, SourceRange


class DiffTest(unittest.TestCase):

    def setUp(self):
        self.file = ["1", "2", "3", "4"]
        self.uut = Diff(self.file)

    def test_add_lines(self):
        self.uut.add_lines(0, [])
        self.uut.add_lines(0, ["t"])
        self.uut.add_lines(0, [])

        # No double addition allowed
        self.assertRaises(ConflictError, self.uut.add_lines, 0, ["t"])
        self.assertRaises(ValueError, self.uut.add_lines, -1, ["t"])
        self.assertRaises(TypeError, self.uut.add_lines, "str", ["t"])

    def test_delete_line(self):
        self.uut.delete_line(1)
        self.uut.delete_line(1)  # Double deletion possible without conflict
        self.assertRaises(ValueError, self.uut.delete_line, 0)

    def test_change_line(self):
        self.assertEqual(len(self.uut), 0)
        self.uut.change_line(2, "1", "2")
        self.assertEqual(len(self.uut), 2)
        self.assertRaises(ConflictError, self.uut.change_line, 2, "1", "3")
        self.assertRaises(ValueError, self.uut.change_line, 0, "1", "2")

        self.uut.delete_line(1)
        # Line was deleted, unchangeable
        self.assertRaises(ConflictError, self.uut.change_line, 1, "1", "2")

    def test_affected_code(self):
        self.assertEqual(self.uut.affected_code("file"), [])

        self.uut.add_lines(0, ["test"])
        affected_code = [
            SourceRange.from_values("file", start_line=1)]
        self.assertEqual(self.uut.affected_code("file"), affected_code)

        self.uut.delete_line(2)
        affected_code = [
            SourceRange.from_values("file", start_line=1),
            SourceRange.from_values("file", start_line=2)]
        self.assertEqual(self.uut.affected_code("file"), affected_code)

        self.uut.delete_line(3)
        affected_code = [
            SourceRange.from_values("file", start_line=1),
            SourceRange.from_values("file", start_line=2, end_line=3)]
        self.assertEqual(self.uut.affected_code("file"), affected_code)

        self.uut.delete_line(6)
        affected_code = [
            SourceRange.from_values("file", start_line=1),
            SourceRange.from_values("file", start_line=2, end_line=3),
            SourceRange.from_values('file', start_line=6)]
        self.assertEqual(self.uut.affected_code("file"), affected_code)

    def test_len(self):
        self.uut.delete_line(2)
        self.assertEqual(len(self.uut), 1)
        self.uut.add_lines(2, ["2.3", "2.5", "2.6"])
        self.assertEqual(len(self.uut), 4)
        self.uut.change_line(1, "1", "1.1")
        self.assertEqual(len(self.uut), 6)

    def test_stats(self):
        self.uut.delete_line(2)
        self.assertEqual(self.uut.stats(), (0, 1))
        self.uut.add_lines(2, ["2.3", "2.5", "2.6"])
        self.assertEqual(self.uut.stats(), (3, 1))
        self.uut.change_line(1, "1", "1.1")
        self.assertEqual(self.uut.stats(), (4, 2))

    def test_modified(self):
        result_file = ["0.1",
                       "0.2",
                       "1",
                       "1.1",
                       "3.changed",
                       "4"]

        self.uut.delete_line(2)
        self.uut.add_lines(0, ["0.1", "0.2"])
        self.uut.add_lines(1, ["1.1"])
        self.uut.change_line(3, "3", "3.changed")
        self.assertEqual(self.uut.modified, result_file)
        self.assertEqual(self.uut.original, self.file)

        self.uut.delete_line(len(self.file))
        del result_file[len(result_file) - 1]
        self.assertEqual(self.uut.modified, result_file)

        self.uut.delete_line(1)
        del result_file[2]
        self.assertEqual(self.uut.modified, result_file)

    def test_addition(self):
        self.assertRaises(TypeError, self.uut.__add__, 5)

        result_file = ["1",
                       "2",
                       "2"]

        other = Diff(self.file)
        other.delete_line(1)
        other.change_line(2, "1", "2")
        other.add_lines(0, ["1"])

        self.uut.delete_line(1)
        self.uut.delete_line(3)
        self.uut.change_line(4, "4", "2")
        result = self.uut + other

        self.assertEqual(result.modified, result_file)
        # Make sure it didn't happen in place!
        self.assertNotEqual(self.uut.modified, result_file)

    def test_addition_rename(self):
        uut = Diff(self.file, rename=False)
        other = Diff(self.file, rename=False)
        self.assertEqual((other + uut).rename, False)

        other.rename = "some.py"
        self.assertEqual((other + uut).rename, "some.py")

        uut.rename = "some.py"
        self.assertEqual((other + uut).rename, "some.py")

        uut.rename = "other.py"
        self.assertRaises(ConflictError, other.__add__, uut)

    def test_from_string_arrays(self):
        a = ["q", "a", "b", "x", "c", "d"]
        b = ["a", "b", "y", "c", "d", "f"]
        self.uut = Diff.from_string_arrays(a, b)
        self.assertEqual(self.uut.modified, b)

        a = ["first", "fourth"]
        b = ["first", "second", "third", "fourth"]
        self.uut = Diff.from_string_arrays(a, b)
        self.assertEqual(self.uut.modified, b)

        a = ["first", "fourth"]
        b = ["first_changed", "second", "third", "fourth"]
        self.uut = Diff.from_string_arrays(a, b)
        self.assertEqual(self.uut.modified, b)

        a = ["first", "second", "third", "fourth"]
        b = ["first", "fourth"]
        self.uut = Diff.from_string_arrays(a, b)
        self.assertEqual(self.uut.modified, b)

        a = ["first", "second", "third", "fourth"]
        b = ["first_changed", "second_changed", "fourth"]
        self.uut = Diff.from_string_arrays(a, b)
        self.assertEqual(self.uut.modified, b)

    def test_from_clang_fixit(self):
        try:
            from clang.cindex import Index, LibclangError
        except ImportError as err:
            raise SkipTest(str(err))

        joined_file = 'struct { int f0; }\nx = { f0 :1 };\n'
        file = joined_file.splitlines(True)
        fixed_file = ['struct { int f0; }\n', 'x = { .f0 = 1 };\n']
        try:
            tu = Index.create().parse('t.c', unsaved_files=[
                ('t.c', joined_file)])
        except LibclangError as err:
            raise SkipTest(str(err))

        fixit = tu.diagnostics[0].fixits[0]
        clang_fixed_file = Diff.from_clang_fixit(fixit, file).modified
        self.assertEqual(fixed_file, clang_fixed_file)

    def test_equality(self):
        a = ["first", "second", "third"]
        b = ["first", "third"]
        diff_1 = Diff.from_string_arrays(a, b)

        a[1] = "else"
        diff_2 = Diff.from_string_arrays(a, b)
        self.assertEqual(diff_1, diff_2)

        diff_1.rename = "abcd"
        self.assertNotEqual(diff_1, diff_2)
        diff_1.rename = False

        diff_1.add_lines(1, ["1"])
        self.assertNotEqual(diff_1, diff_2)

    def test_json_export(self):
        JSONEncoder = create_json_encoder()
        a = ["first\n", "second\n", "third\n"]
        b = ["first\n", "third\n"]
        diff = Diff.from_string_arrays(a, b)
        self.assertEqual(
            json.dumps(diff, cls=JSONEncoder, sort_keys=True),
            '"--- \\n'
            '+++ \\n'
            '@@ -1,3 +1,2 @@\\n'
            ' first\\n'
            '-second\\n'
            ' third\\n"')

    def test_rename(self):
        self.uut.rename = False
        self.uut.rename = "1234"
        with self.assertRaises(TypeError):
            self.uut.rename = True
        with self.assertRaises(TypeError):
            self.uut.rename = 1234
