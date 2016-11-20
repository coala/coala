import json
import unittest
from unittest.case import SkipTest

from coalib.output.JSONEncoder import create_json_encoder
from coalib.results.Diff import ConflictError, Diff, SourceRange
from coalib.results.Diff import coala_unified_diff


class DiffTest(unittest.TestCase):

    def setUp(self):
        self.file = ['1', '2', '3', '4']
        self.uut = Diff(self.file)

    def test_add_lines(self):
        self.uut.add_lines(0, [])
        self.uut.add_lines(0, ['t'])
        self.uut.add_lines(0, [])

    def test_double_addition(self):
        self.uut.add_lines(0, ['t'])

        # No double addition allowed
        self.assertRaises(ConflictError, self.uut.add_lines, 0, ['t'])
        self.assertRaises(ValueError, self.uut.add_lines, -1, ['t'])
        self.assertRaises(TypeError, self.uut.add_lines, 'str', ['t'])

    def test_delete_line(self):
        self.uut.delete_line(1)
        self.uut.delete_line(1)  # Double deletion possible without conflict
        additions, deletions = self.uut.stats()
        self.assertEqual(deletions, 1)
        self.assertRaises(ValueError, self.uut.delete_line, 0)

    def test_delete_lines(self):
        self.uut.delete_lines(1, 10)
        self.uut.delete_lines(10, 20)
        additions, deletions = self.uut.stats()
        self.assertEqual(deletions, 20)
        self.assertRaises(ValueError, self.uut.delete_lines, 0, 10)

    def test_change_line(self):
        self.assertEqual(len(self.uut), 0)
        self.uut.change_line(2, '1', '2')
        self.assertEqual(len(self.uut), 2)
        self.assertRaises(ConflictError, self.uut.change_line, 2, '1', '3')
        self.assertRaises(ValueError, self.uut.change_line, 0, '1', '2')

        self.uut.delete_line(1)
        # Line was deleted, unchangeable
        self.assertRaises(ConflictError, self.uut.change_line, 1, '1', '2')

    def test_double_changes_with_same_diff(self):
        self.uut.change_line(2, '1', '2')

        # Double addition when diff is equal is allowed
        try:
            self.uut.change_line(2, '1', '2')
        except Exception:
            self.fail('We should not have a conflict on same diff!')

    def test_affected_code(self):
        self.assertEqual(self.uut.affected_code('file'), [])

        self.uut.add_lines(0, ['test'])
        affected_code = [
            SourceRange.from_values('file', start_line=1)]
        self.assertEqual(self.uut.affected_code('file'), affected_code)

        self.uut.delete_line(2)
        affected_code = [
            SourceRange.from_values('file', start_line=1),
            SourceRange.from_values('file', start_line=2)]
        self.assertEqual(self.uut.affected_code('file'), affected_code)

        self.uut.delete_line(3)
        affected_code = [
            SourceRange.from_values('file', start_line=1),
            SourceRange.from_values('file', start_line=2, end_line=3)]
        self.assertEqual(self.uut.affected_code('file'), affected_code)

        self.uut.delete_line(6)
        affected_code = [
            SourceRange.from_values('file', start_line=1),
            SourceRange.from_values('file', start_line=2, end_line=3),
            SourceRange.from_values('file', start_line=6)]
        self.assertEqual(self.uut.affected_code('file'), affected_code)

    def test_len(self):
        self.uut.delete_line(2)
        self.assertEqual(len(self.uut), 1)
        self.uut.add_lines(2, ['2.3', '2.5', '2.6'])
        self.assertEqual(len(self.uut), 4)
        self.uut.change_line(1, '1', '1.1')
        self.assertEqual(len(self.uut), 6)

    def test_stats(self):
        self.uut.delete_line(2)
        self.assertEqual(self.uut.stats(), (0, 1))
        self.uut.add_lines(2, ['2.3', '2.5', '2.6'])
        self.assertEqual(self.uut.stats(), (3, 1))
        self.uut.change_line(1, '1', '1.1')
        self.assertEqual(self.uut.stats(), (4, 2))

    def test_modified(self):
        result_file = ['0.1',
                       '0.2',
                       '1',
                       '1.1',
                       '3.changed',
                       '4']

        self.uut.delete_line(2)
        self.uut.add_lines(0, ['0.1', '0.2'])
        self.uut.add_lines(1, ['1.1'])
        self.uut.change_line(3, '3', '3.changed')

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

        result_file = ['1',
                       '2',
                       '2']

        other = Diff(self.file)
        other.delete_line(1)
        other.change_line(2, '1', '2')
        other.add_lines(0, ['1'])

        self.uut.delete_line(1)
        self.uut.delete_line(3)
        self.uut.change_line(4, '4', '2')
        result = self.uut + other

        self.assertEqual(result.modified, result_file)
        # Make sure it didn't happen in place!
        self.assertNotEqual(self.uut.modified, result_file)

    def test_addition_rename(self):
        uut = Diff(self.file, rename=False)
        other = Diff(self.file, rename=False)
        self.assertEqual((other + uut).rename, False)

        other.rename = 'some.py'
        self.assertEqual((other + uut).rename, 'some.py')

        uut.rename = 'some.py'
        self.assertEqual((other + uut).rename, 'some.py')

        uut.rename = 'other.py'
        self.assertRaises(ConflictError, other.__add__, uut)

    def test_from_string_arrays(self):
        a = ['q', 'a', 'b', 'x', 'c', 'd']
        b = ['a', 'b', 'y', 'c', 'd', 'f']
        self.uut = Diff.from_string_arrays(a, b)
        self.assertEqual(self.uut.modified, b)

        a = ['first', 'fourth']
        b = ['first', 'second', 'third', 'fourth']
        self.uut = Diff.from_string_arrays(a, b)
        self.assertEqual(self.uut.modified, b)

        a = ['first', 'fourth']
        b = ['first_changed', 'second', 'third', 'fourth']
        self.uut = Diff.from_string_arrays(a, b)
        self.assertEqual(self.uut.modified, b)

        a = ['first', 'second', 'third', 'fourth']
        b = ['first', 'fourth']
        self.uut = Diff.from_string_arrays(a, b)
        self.assertEqual(self.uut.modified, b)

        a = ['first', 'second', 'third', 'fourth']
        b = ['first_changed', 'second_changed', 'fourth']
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
        a = ['first', 'second', 'third']
        b = ['first', 'third']
        diff_1 = Diff.from_string_arrays(a, b)

        a[1] = 'else'
        diff_2 = Diff.from_string_arrays(a, b)
        self.assertEqual(diff_1, diff_2)

        diff_1.rename = 'abcd'
        self.assertNotEqual(diff_1, diff_2)
        diff_1.rename = False

        diff_1.delete = True
        self.assertNotEqual(diff_1, diff_2)
        diff_1.delete = False

        diff_1.add_lines(1, ['1'])
        self.assertNotEqual(diff_1, diff_2)

    def test_json_export(self):
        JSONEncoder = create_json_encoder()
        a = ['first\n', 'second\n', 'third\n']
        b = ['first\n', 'third\n']
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
        self.uut.rename = '1234'
        with self.assertRaises(TypeError):
            self.uut.rename = True
        with self.assertRaises(TypeError):
            self.uut.rename = 1234

    def test_delete(self):
        self.uut.delete = True
        self.uut.delete = False
        # Double deletion is allowed
        self.uut.delete = False
        with self.assertRaises(TypeError):
            self.uut.delete = 'abcd'

        # If delete is True then modified returns an empty list
        self.uut.delete = True
        self.assertEqual(self.uut.modified, [])
        self.uut.delete = False

    def test_unified_diff(self):
        """ Test no newline at end of file, from https://github.com/coala/coala/issues/2006 """

        with_no_new_lines = list(coala_unified_diff(
            "one\ntwo\nthree".splitlines(1),
            "one\ntwo\ntrois".splitlines(1),
            "Before", "After"))
        with_no_new_lines_expected = [
            '--- Before\n',
            '+++ After\n',
            '@@ -1,3 +1,3 @@\n',
            ' one\n',
            ' two\n',
            '-three\n',
            '\\ No newline at end of file\n',
            '+trois\n',
            '\\ No newline at end of file\n'
        ]
        self.assertEqual(with_no_new_lines, with_no_new_lines_expected)
        with_new_lines = list(coala_unified_diff(
            "one\ntwo\nthree\n".splitlines(1),
            "one\ntwo\ntrois\n".splitlines(1),
            "Before", "After"))
        with_new_lines_expected = [
            '--- Before\n',
            '+++ After\n',
            '@@ -1,3 +1,3 @@\n',
            ' one\n',
            ' two\n',
            '-three\n',
            '+trois\n'
        ]
        self.assertEqual(with_new_lines, with_new_lines_expected)
        all_equal_lines1 = list(coala_unified_diff(
            "one\ntwo\nthree\n".splitlines(1),
            "one\ntwo\nthree".splitlines(1),
            "Before", "After"))
        all_equal_lines_expected1 = [
            '--- Before\n',
            '+++ After\n',
            '@@ -1,3 +1,3 @@\n',
            ' one\n',
            ' two\n',
            '-three\n',
            '+three\n',
            '\\ No newline at end of file\n'
        ]
        self.assertEqual(all_equal_lines1, all_equal_lines_expected1)
        all_equal_lines2 = list(coala_unified_diff(
            "one\ntwo\nthree".splitlines(1),
            "one\ntwo\nthree\n".splitlines(1),
            "Before", "After"))
        all_equal_lines_expected2 = [
            '--- Before\n',
            '+++ After\n',
            '@@ -1,3 +1,3 @@\n',
            ' one\n',
            ' two\n',
            '-three\n',
            '\\ No newline at end of file\n',
            '+three\n'
        ]
        self.assertEqual(all_equal_lines2, all_equal_lines_expected2)
        insert_lines = list(coala_unified_diff(
            "one\ntwo\nthree".splitlines(1),
            "one\ntwo\nthree\n".splitlines(1),
            "Before", "After"))
        insert_lines_expected = [
            '--- Before\n',
            '+++ After\n',
            '@@ -1,3 +1,3 @@\n',
            ' one\n',
            ' two\n',
            '-three\n',
            '\\ No newline at end of file\n',
            '+three\n'
        ]
        self.assertEqual(insert_lines, insert_lines_expected)
        del_lines = list(coala_unified_diff(
            "one\ntwo".splitlines(1),
            "one\n".splitlines(1),
            "Before", "After"))
        del_lines_expected = [
            '--- Before\n',
            '+++ After\n',
            '@@ -1,2 +1,1 @@\n',
            ' one\n',
            '-two\n',
            '\\ No newline at end of file\n'
        ]
        self.assertEqual(del_lines, del_lines_expected)
        ins_lines = list(coala_unified_diff(
            "one\ntwo\n".splitlines(1),
            "one\ntwo\nthree".splitlines(1),
            "Before", "After", '2016-01-26 23:30:50', '2016-04-02 10:20:52'))
        ins_lines_expected = [
            '--- Before\t2016-01-26 23:30:50\n',
            '+++ After\t2016-04-02 10:20:52\n',
            '@@ -1,2 +1,3 @@\n',
            ' one\n',
            ' two\n',
            '+three\n',
            '\\ No newline at end of file\n'
        ]
        self.assertEqual(ins_lines, ins_lines_expected)
        a = list(map(str, range(1, 40)))
        b = a[:]
        b[8:8] = ['i']
        b[20] += 'x'
        b[23:28] = []
        b[30] += 'y'
        groups_check_lines = list(coala_unified_diff(
            a, b,
            "Before", "After", '2016-01-26 23:30:50', '2016-04-02 10:20:52'))
        groups_check_lines_expected = [
            '--- Before\t2016-01-26 23:30:50\n',
            '+++ After\t2016-04-02 10:20:52\n',
            '@@ -6,6 +6,7 @@\n', ' 6', ' 7', ' 8', '+i\n',
            '\\ No newline at end of file\n', ' 9', ' 10', ' 11',
            '@@ -17,14 +18,9 @@\n', ' 17', ' 18', ' 19', '-20\n',
            '\\ No newline at end of file\n', '+20x\n',
            '\\ No newline at end of file\n', ' 21', ' 22', '-23\n',
            '\\ No newline at end of file\n',
            '-24\n', '\\ No newline at end of file\n', '-25\n',
            '\\ No newline at end of file\n', '-26\n',
            '\\ No newline at end of file\n', '-27\n',
            '\\ No newline at end of file\n', ' 28', ' 29',
            ' 30', '@@ -32,7 +28,7 @@\n', ' 32', ' 33', ' 34', '-35\n',
            '\\ No newline at end of file\n', '+35y\n',
            '\\ No newline at end of file\n', ' 36', ' 37', ' 38']
        self.assertEqual(groups_check_lines, groups_check_lines_expected)
