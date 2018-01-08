import json
import logging
import unittest
import unittest.case

from unidiff.errors import UnidiffParseError

from coalib.output.JSONEncoder import create_json_encoder
from coalib.results.Diff import ConflictError, Diff, SourceRange


class DiffTest(unittest.TestCase):

    def setUp(self):
        self.file = ['1', '2', '3', '4']
        self.uut = Diff(self.file)

    def test_add_lines(self):
        self.uut.add_lines(0, [])
        self.uut.add_lines(0, ['t'])
        self.uut.add_lines(0, [])

    def test_add_line(self):
        self.uut.add_line(0, 't')
        self.assertRaises(ConflictError, self.uut.add_line, 0, 't')
        self.assertEqual(self.uut.modified, ['t\n', '1\n', '2\n', '3\n', '4'])

    def test_double_addition(self):
        self.uut.add_lines(0, ['t'])

        # No double addition allowed
        self.assertRaises(ConflictError, self.uut.add_lines, 0, ['t'])
        self.assertRaises(IndexError, self.uut.add_lines, -1, ['t'])
        self.assertRaises(TypeError, self.uut.add_lines, 'str', ['t'])

    def test_delete_line(self):
        self.uut.delete_line(1)
        self.uut.delete_line(1)  # Double deletion possible without conflict
        additions, deletions = self.uut.stats()
        self.assertEqual(deletions, 1)
        self.assertRaises(IndexError, self.uut.delete_line, 0)
        self.assertRaises(IndexError, self.uut.delete_line, 10)

    def test_delete_lines(self):
        self.uut.delete_lines(1, 2)
        self.uut.delete_lines(2, 3)
        additions, deletions = self.uut.stats()
        self.assertEqual(deletions, 3)
        self.assertRaises(IndexError, self.uut.delete_lines, 0, 2)
        self.assertRaises(IndexError, self.uut.delete_lines, 1, 6)

    def test_change_line(self):
        self.assertEqual(len(self.uut), 0)
        self.uut.change_line(2, '1', '2')
        self.assertEqual(len(self.uut), 2)
        self.assertRaises(ConflictError, self.uut.change_line, 2, '1', '3')
        self.assertRaises(IndexError, self.uut.change_line, 0, '1', '2')

        self.uut.delete_line(1)
        # Line was deleted, unchangeable
        self.assertRaises(ConflictError, self.uut.change_line, 1, '1', '2')

    def test_capture_warnings(self):
        """
        Since this addresses the deprecated method, this testcase is
        temporary (until the old API is fully removed).
        """
        logger = logging.getLogger()
        with self.assertLogs(logger, 'DEBUG') as log:
            self.assertEqual(len(self.uut), 0)
            self.uut.change_line(2, '1', '2')
        self.assertEqual(log.output, [
            'DEBUG:root:Use of change_line method is deprecated. Instead '
            'use modify_line method, without the original_line argument'])

    def test_double_changes_with_same_diff(self):
        self.uut.modify_line(2, '2')

        # Double addition when diff is equal is allowed
        try:
            self.uut.modify_line(2, '2')
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

        self.uut.delete_line(4)
        affected_code = [
            SourceRange.from_values('file', start_line=1),
            SourceRange.from_values('file', start_line=2, end_line=4)]
        self.assertEqual(self.uut.affected_code('file'), affected_code)

    def test_len(self):
        self.uut.delete_line(2)
        self.assertEqual(len(self.uut), 1)
        self.uut.add_lines(2, ['2.3', '2.5', '2.6'])
        self.assertEqual(len(self.uut), 4)
        self.uut.modify_line(1, '1.1')
        self.assertEqual(len(self.uut), 6)

    def test_stats(self):
        self.uut.delete_line(2)
        self.assertEqual(self.uut.stats(), (0, 1))
        self.uut.add_lines(2, ['2.3', '2.5', '2.6'])
        self.assertEqual(self.uut.stats(), (3, 1))
        self.uut.modify_line(1, '1.1')
        self.assertEqual(self.uut.stats(), (4, 2))

    def test_modified(self):
        result_file = ['0.1\n',
                       '0.2\n',
                       '1\n',
                       '1.1\n',
                       '3.changed\n',
                       '4']

        self.uut.delete_line(2)
        self.uut.add_lines(0, ['0.1', '0.2'])
        self.uut.add_lines(1, ['1.1'])
        self.uut.modify_line(3, '3.changed')

        self.assertEqual(self.uut.modified, result_file)

        self.uut.delete_line(len(self.file))
        del result_file[-1]
        result_file[-1] = result_file[-1].rstrip('\n')
        self.assertEqual(self.uut.modified, result_file)

        self.uut.delete_line(1)
        del result_file[2]
        self.assertEqual(self.uut.modified, result_file)

    def test_bool(self):
        self.assertFalse(self.uut)
        self.uut.add_line(4, '4')
        self.assertTrue(self.uut)
        self.uut.delete_line(4)
        self.assertFalse(self.uut)
        self.uut.modify_line(1, '1\n')
        self.assertFalse(self.uut)

        # test if it works with tuples.
        uutuple = Diff(('1', '2', '3', '4'))

        self.assertFalse(uutuple)
        uutuple.add_line(4, '4')
        self.assertTrue(uutuple)
        uutuple.delete_line(4)
        self.assertFalse(uutuple)
        uutuple.modify_line(1, '1\n')
        self.assertFalse(uutuple)

    def test_addition(self):
        self.assertRaises(TypeError, self.uut.__add__, 5)

        result_file = ['1\n',
                       '2\n',
                       '2']

        other = Diff(self.file)
        other.delete_line(1)
        other.modify_line(2, '2')
        other.add_lines(0, ['1'])

        self.uut.delete_line(1)
        self.uut.delete_line(3)
        self.uut.modify_line(4, '2')
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
        a = ['q\n', 'a\n', 'b\n', 'x\n', 'c\n', 'd\n']
        b = ['a\n', 'b\n', 'y\n', 'c\n', 'd\n', 'f\n']
        self.uut = Diff.from_string_arrays(a, b)
        self.assertEqual(self.uut.modified, b)

        a = ['first\n', 'fourth\n']
        b = ['first\n', 'second\n', 'third\n', 'fourth\n']
        self.uut = Diff.from_string_arrays(a, b)
        self.assertEqual(self.uut.modified, b)

        a = ['first\n', 'fourth\n']
        b = ['first_changed\n', 'second\n', 'third\n', 'fourth\n']
        self.uut = Diff.from_string_arrays(a, b)
        self.assertEqual(self.uut.modified, b)

        a = ['first\n', 'second\n', 'third\n', 'fourth\n']
        b = ['first\n', 'fourth\n']
        self.uut = Diff.from_string_arrays(a, b)
        self.assertEqual(self.uut.modified, b)

        a = ['first\n', 'second\n', 'third\n', 'fourth\n']
        b = ['first_changed\n', 'second_changed\n', 'fourth\n']
        self.uut = Diff.from_string_arrays(a, b)
        self.assertEqual(self.uut.modified, b)

    def test_from_unified_diff_single_addition(self):
        source = ['single line']
        target = ['single line\n', 'another line added']
        diff = ['--- a/testfile',
                '+++ b/testfile',
                '@@ -1 +1,2 @@',
                ' single line',
                '+another line added']
        diff_string = '\n'.join(diff)
        self.uut = Diff.from_unified_diff(diff_string, source)
        self.assertEqual(self.uut.original, source)
        self.assertEqual(self.uut.modified, target)

    def test_from_unified_diff_single_deletion(self):
        source = ['two lines\n', 'to be removed']
        target = ['two lines\n']
        diff = ['--- a/testfile',
                '+++ b/testfile',
                '@@ -1,2 +1 @@',
                ' two lines',
                '-to be removed']
        diff_string = '\n'.join(diff)
        self.uut = Diff.from_unified_diff(diff_string, source)
        self.assertEqual(self.uut.original, source)
        self.assertEqual(self.uut.modified, target)

    def test_from_unified_diff_single_modification(self):
        source = ['first\n', 'second']
        target = ['only_first_changed\n', 'second']
        diff = ['--- a/testfile',
                '+++ b/testfile',
                '@@ -1,2 +1,2 @@',
                '-first',
                '+only_first_changed',
                ' second']
        diff_string = '\n'.join(diff)
        self.uut = Diff.from_unified_diff(diff_string, source)
        self.assertEqual(self.uut.original, source)
        self.assertEqual(self.uut.modified, target)

    def test_from_unified_diff_multiple_additions_different_orderings(self):
        source = ['A\n', 'B\n', 'C']
        target = ['A\n', 'Y\n', 'Z\n', 'B\n', 'C']
        diff = ['--- a/testfile',
                '+++ b/testfile',
                '@@ -1,3 +1,5 @@',
                ' A',
                '+Y',
                '+Z',
                ' B',
                ' C']
        diff_string = '\n'.join(diff)
        self.uut = Diff.from_unified_diff(diff_string, source)
        self.assertEqual(self.uut.original, source)
        self.assertEqual(self.uut.modified, target)

        source = ['A\n', 'B\n', 'C']
        target = ['A\n', 'Y\n', 'Z\n', 'C']
        diff = ['--- a/testfile',
                '+++ b/testfile',
                '@@ -1,3 +1,4 @@',
                ' A',
                '+Y',
                '+Z',
                '-B',
                ' C']
        diff_string = '\n'.join(diff)
        self.uut = Diff.from_unified_diff(diff_string, source)
        self.assertEqual(self.uut.original, source)
        self.assertEqual(self.uut.modified, target)

        source = ['A\n', 'B\n', 'C']
        target = ['Y\n', 'Z\n', 'C']
        diff = ['--- a/testfile',
                '+++ b/testfile',
                '@@ -1,3 +1,3 @@',
                '-A',
                '+Y',
                '+Z',
                '-B',
                ' C']
        diff_string = '\n'.join(diff)
        self.uut = Diff.from_unified_diff(diff_string, source)
        self.assertEqual(self.uut.original, source)
        self.assertEqual(self.uut.modified, target)

        source = ['A\n', 'B\n', 'C']
        target = ['A\n', 'B\n', 'C\n', 'Y\n', 'Z']
        diff = ['--- a/testfile',
                '+++ b/testfile',
                '@@ -3 +3,3 @@',
                ' C',
                '+Y',
                '+Z']
        diff_string = '\n'.join(diff)
        self.uut = Diff.from_unified_diff(diff_string, source)
        self.assertEqual(self.uut.original, source)
        self.assertEqual(self.uut.modified, target)

    def test_from_unified_diffrent_beginning_line_types(self):
        source = ['A\n', 'B\n', 'C']
        target = ['A\n', 'Y\n', 'B\n', 'C']
        diff = ['--- a/testfile',
                '+++ b/testfile',
                '@@ -1,3 +1,4 @@',
                ' A',
                '+Y',
                ' B',
                ' C']
        diff_string = '\n'.join(diff)
        self.uut = Diff.from_unified_diff(diff_string, source)
        self.assertEqual(self.uut.original, source)
        self.assertEqual(self.uut.modified, target)

        source = ['A\n', 'B\n', 'C']
        target = ['B\n', 'C']
        diff = ['--- a/testfile',
                '+++ b/testfile',
                '@@ -1,3 +1,2 @@',
                '-A',
                ' B',
                ' C']
        diff_string = '\n'.join(diff)
        self.uut = Diff.from_unified_diff(diff_string, source)
        self.assertEqual(self.uut.original, source)
        self.assertEqual(self.uut.modified, target)

        source = ['A\n', 'B\n', 'C']
        target = ['Z\n', 'A\n', 'B\n', 'C']
        diff = ['--- a/testfile',
                '+++ b/testfile',
                '@@ -1,2 +1,3 @@',
                '+Z',
                ' A',
                ' B']
        diff_string = '\n'.join(diff)
        self.uut = Diff.from_unified_diff(diff_string, source)
        self.assertEqual(self.uut.original, source)
        self.assertEqual(self.uut.modified, target)

    def test_from_unified_diff_multiple_modifications(self):
        source = ['first\n', 'second']
        target = ['first_changed\n', 'second_changed']
        diff = ['--- a/testfile',
                '+++ b/testfile',
                '@@ -1,2 +1,2 @@',
                '-first',
                '-second',
                '+first_changed',
                '+second_changed']
        diff_string = '\n'.join(diff)
        self.uut = Diff.from_unified_diff(diff_string, source)
        self.assertEqual(self.uut.original, source)
        self.assertEqual(self.uut.modified, target)

    def test_from_unified_diff_multiple_hunks(self):
        source = ['A\n', 'B\n', 'C\n', 'D\n', 'E\n', 'F\n', 'G']
        target = ['A\n', 'C\n', 'D\n', 'E\n', 'F\n']
        diff = ['--- a/testfile',
                '+++ b/testfile',
                '@@ -1,2 +1,1 @@',
                ' A',
                '-B',
                '@@ -3,5 +2,4 @@',
                ' C',
                ' D',
                ' E',
                ' F',
                '-G']
        diff_string = '\n'.join(diff)
        self.uut = Diff.from_unified_diff(diff_string, source)
        self.assertEqual(self.uut.original, source)
        self.assertEqual(self.uut.modified, target)

    def test_from_unified_diff_incomplete_hunks_multiple_deletions(self):
        source = ['A\n', 'B\n', 'C\n', 'D\n', 'E\n', 'F\n', 'G']
        target = ['A\n', 'C\n', 'D\n', 'E\n', 'F\n']
        diff = ['--- a/testfile',
                '+++ b/testfile',
                '@@ -1,2 +1,1 @@',
                ' A',
                '-B',
                '@@ -5,3 +4,2 @@',
                ' E',
                ' F',
                '-G']
        diff_string = '\n'.join(diff)
        self.uut = Diff.from_unified_diff(diff_string, source)
        self.assertEqual(self.uut.original, source)
        self.assertEqual(self.uut.modified, target)

    def test_from_unified_diff_incomplete_hunks_multiple_additions(self):
        source = ['A\n', 'C\n', 'D\n', 'E\n', 'G']
        target = ['A\n', 'B\n', 'C\n', 'D\n', 'E\n', 'F\n', 'G']
        diff = ['--- a/testfile',
                '+++ b/testfile',
                '@@ -1,1 +1,2 @@',
                ' A',
                '+B',
                '@@ -4,2 +5,3 @@',
                ' E',
                '+F',
                ' G']
        diff_string = '\n'.join(diff)
        self.uut = Diff.from_unified_diff(diff_string, source)
        self.assertEqual(self.uut.original, source)
        self.assertEqual(self.uut.modified, target)

    def test_from_unified_diff_incomplete_hunks_multiple_modifications(self):
        source = ['A\n', 'B\n', 'C\n', 'D\n', 'E\n', 'F\n', 'G']
        target = ['A\n', 'B\n', 'Z\n', 'D\n', 'E\n', 'F\n', 'K']
        diff = ['--- a/testfile',
                '+++ b/testfile',
                '@@ -1,3 +1,3 @@',
                ' A',
                ' B',
                '-C',
                '+Z',
                '@@ -6,2 +5,2 @@',
                ' F',
                '-G',
                '+K']
        diff_string = '\n'.join(diff)
        self.uut = Diff.from_unified_diff(diff_string, source)
        self.assertEqual(self.uut.original, source)
        self.assertEqual(self.uut.modified, target)

    def test_from_unified_diff_unmatched_line_to_delete(self):
        source = ['first', 'second']
        diff = ['--- a/testfile',
                '+++ b/testfile',
                '@@ -1,2 +1,2 @@',
                '-line_to_be_deleted_is_not_same',
                '+only_first_changed',
                ' second']
        diff_string = '\n'.join(diff)

        error_message = ('The line to delete does not match with '
                         'the line in the original file. '
                         'Line to delete: {!r}, '
                         'Original line #{!r}: {!r}')

        with self.assertRaisesRegex(
                RuntimeError,
                error_message.format(
                    'line_to_be_deleted_is_not_same',
                    1,
                    'first')):
            Diff.from_unified_diff(diff_string, source)

    def test_from_unified_diff_unmatched_context_line(self):
        source = ['first', 'second']
        diff = ['--- a/testfile',
                '+++ b/testfile',
                '@@ -1,2 +1,2 @@',
                ' context_line_is_not_same',
                ' second']
        diff_string = '\n'.join(diff)

        error_message = ('Context lines do not match. '
                         'Line from unified diff: {!r}, '
                         'Original line #{!r}: {!r}')

        with self.assertRaisesRegex(
            RuntimeError,
            error_message.format(
                'context_line_is_not_same',
                1,
                'first')):
            Diff.from_unified_diff(diff_string, source)

    def test_from_unified_diff_no_changes(self):
        source = ['first\n', 'second']
        target = ['first\n', 'second']
        diff = ['--- a/testfile',
                '+++ b/testfile',
                '@@ -1,2 +1,2 @@',
                ' first',
                ' second']
        diff_string = '\n'.join(diff)
        self.uut = Diff.from_unified_diff(diff_string, source)
        self.assertEqual(self.uut.original, source)
        self.assertEqual(self.uut.modified, target)

    def test_from_unified_diff_no_changes_empty_diff(self):
        source = ['first\n', 'second']
        target = ['first\n', 'second']
        diff_string = ''
        self.uut = Diff.from_unified_diff(diff_string, source)
        self.assertEqual(self.uut.original, source)
        self.assertEqual(self.uut.modified, target)

    def test_from_unified_diff_invalid_line_type_character(self):
        source = ['first', 'invalid starting character']
        diff = ['--- a/testfile',
                '+++ b/testfile',
                '@@ -1,2 +1,2 @@',
                ' first',
                '*invalid_starting_character']
        diff_string = '\n'.join(diff)
        with self.assertRaises(UnidiffParseError):
            self.uut = Diff.from_unified_diff(diff_string, source)

    def test_from_unified_diff_invalid_hunk(self):
        source = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        diff = ['--- a/testfile',
                '+++ b/testfile',
                '@@ -1,7 +1,5 @@',
                ' A',
                ' B',
                '-C',
                '+Z',
                '@@ -6,2 +5,2 @@',
                ' F',
                '-G',
                '+K']
        diff_string = '\n'.join(diff)
        with self.assertRaises(UnidiffParseError):
            self.uut = Diff.from_unified_diff(diff_string, source)

    def test_from_clang_fixit(self):
        try:
            from clang.cindex import Index, LibclangError
        except ImportError as err:
            raise unittest.case.SkipTest(str(err))

        joined_file = 'struct { int f0; }\nx = { f0 :1 };\n'
        file = joined_file.splitlines(True)
        fixed_file = ['struct { int f0; }\n', 'x = { .f0 = 1 };\n']
        try:
            tu = Index.create().parse('t.c', unsaved_files=[
                ('t.c', joined_file)])
        except LibclangError as err:
            raise unittest.case.SkipTest(str(err))

        fixit = tu.diagnostics[0].fixits[0]
        clang_fixed_file = Diff.from_clang_fixit(fixit, file).modified
        self.assertEqual(fixed_file, clang_fixed_file)

    def test_equality(self):
        a = ['first', 'second', 'third']
        b = ['first', 'third']
        diff_1 = Diff.from_string_arrays(a, b)

        c = ['first', 'second', 'third']
        d = ['first', 'third']

        diff_2 = Diff.from_string_arrays(c, d)

        self.assertEqual(diff_1, diff_2)

        # changing the original array should not influence
        # the diff
        a[1] = 'else'
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

    def test_add_linebreaks(self):
        expected = ['1\n', '2\n', '3\n']

        self.assertEqual(
            Diff._add_linebreaks(['1', '2', '3']),
            expected)

        self.assertEqual(
            Diff._add_linebreaks(['1', '2\n', '3']),
            expected)

        self.assertEqual(
            Diff._add_linebreaks(expected),
            expected)

        self.assertEqual(Diff._add_linebreaks([]), [])

    def test_generate_linebreaks(self):
        eof_ln = ['1\n', '2\n', '3\n']
        no_eof_ln = ['1\n', '2\n', '3']

        self.assertEqual(
            Diff._generate_linebreaks(['1', '2', '3']),
            no_eof_ln)

        self.assertEqual(
            Diff._generate_linebreaks(['1', '2', '3\n']),
            eof_ln)

        self.assertEqual(
            Diff._generate_linebreaks(['1', '2\n', '3']),
            no_eof_ln)

        self.assertEqual(
            Diff._generate_linebreaks(no_eof_ln),
            no_eof_ln)

        self.assertEqual(
            Diff._generate_linebreaks(eof_ln),
            eof_ln)

        self.assertEqual(Diff._generate_linebreaks([]), [])
