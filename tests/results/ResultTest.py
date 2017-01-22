import unittest
import json
from os.path import abspath

from coalib.results.Diff import Diff
from coalib.results.Result import RESULT_SEVERITY, Result
from coalib.results.SourceRange import SourceRange
from coalib.output.JSONEncoder import create_json_encoder


class ResultTest(unittest.TestCase):

    def test_origin(self):
        uut = Result('origin', 'msg')
        self.assertEqual(uut.origin, 'origin')

        uut = Result(self, 'msg')
        self.assertEqual(uut.origin, 'ResultTest')

        uut = Result(None, 'msg')
        self.assertEqual(uut.origin, '')

    def test_invalid_severity(self):
        with self.assertRaises(ValueError):
            Result('o', 'm', severity=-5)

    def test_invalid_confidence(self):
        with self.assertRaises(ValueError):
            Result('o', 'm', confidence=-1)
        with self.assertRaises(ValueError):
            Result('o', 'm', confidence=101)

    def test_message_arguments(self):
        uut = Result('origin', '{msg}', message_arguments={'msg': 'msg'})
        self.assertEqual(uut.message, 'msg')

        with self.assertRaises(KeyError):
            Result('origin', '{msg}', message_arguments={'message': 'msg'})

    def test_string_dict(self):
        uut = Result(None, '')
        output = uut.to_string_dict()
        self.assertEqual(output, {'id': str(uut.id),
                                  'origin': '',
                                  'message': '',
                                  'file': '',
                                  'line_nr': '',
                                  'severity': 'NORMAL',
                                  'debug_msg': '',
                                  'additional_info': '',
                                  'confidence': '100',
                                  'message_base': '',
                                  'message_arguments': '{}'})

        uut = Result.from_values(origin='origin',
                                 message='{test} msg',
                                 message_arguments={'test': 'test'},
                                 file='file',
                                 line=2,
                                 severity=RESULT_SEVERITY.INFO,
                                 additional_info='hi!',
                                 debug_msg='dbg',
                                 confidence=50)
        output = uut.to_string_dict()
        self.assertEqual(output, {'id': str(uut.id),
                                  'origin': 'origin',
                                  'message': 'test msg',
                                  'file': abspath('file'),
                                  'line_nr': '2',
                                  'severity': 'INFO',
                                  'debug_msg': 'dbg',
                                  'additional_info': 'hi!',
                                  'confidence': '50',
                                  'message_base': '{test} msg',
                                  'message_arguments': '{\'test\': \'test\'}'})

        uut = Result.from_values(origin='o', message='m', file='f', line=5)
        output = uut.to_string_dict()
        self.assertEqual(output['line_nr'], '5')

    def test_apply(self):
        file_dict = {
            'f_a': ['1', '2', '3'],
            'f_b': ['1', '2', '3']
        }
        expected_file_dict = {
            'f_a': ['1', '3_changed'],
            'f_b': ['1', '2', '3']
        }
        diff = Diff(file_dict['f_a'])
        diff.delete_line(2)
        diff.change_line(3, '3', '3_changed')

        uut = Result('origin', 'msg', diffs={'f_a': diff})
        uut.apply(file_dict)

        self.assertEqual(file_dict, expected_file_dict)

    def test_add(self):
        file_dict = {
            'f_a': ['1', '2', '3'],
            'f_b': ['1', '2', '3'],
            'f_c': ['1', '2', '3']
        }
        expected_file_dict = {
            'f_a': ['1', '3_changed'],
            'f_b': ['1', '2', '3_changed'],
            'f_c': ['1', '2', '3']
        }

        diff = Diff(file_dict['f_a'])
        diff.delete_line(2)
        uut1 = Result('origin', 'msg', diffs={'f_a': diff})

        diff = Diff(file_dict['f_a'])
        diff.change_line(3, '3', '3_changed')
        uut2 = Result('origin', 'msg', diffs={'f_a': diff})

        diff = Diff(file_dict['f_b'])
        diff.change_line(3, '3', '3_changed')
        uut3 = Result('origin', 'msg', diffs={'f_b': diff})

        uut1 += uut2 + uut3
        uut1.apply(file_dict)

        self.assertEqual(file_dict, expected_file_dict)

    def test_overlaps(self):
        overlapping_range = SourceRange.from_values('file1', 1, 1, 2, 2)
        nonoverlapping_range = SourceRange.from_values('file2', 1, 1, 2, 2)
        uut = Result.from_values('origin',
                                 'message',
                                 file='file1',
                                 line=1,
                                 column=1,
                                 end_line=2,
                                 end_column=2)
        self.assertTrue(uut.overlaps(overlapping_range))
        self.assertTrue(uut.overlaps([overlapping_range]))
        self.assertFalse(uut.overlaps(nonoverlapping_range))

    def test_location_repr(self):
        result_a = Result(origin='o', message='m')
        self.assertEqual(result_a.location_repr(), 'the whole project')

        result_b = Result.from_values('o', 'm', file='e')
        self.assertEqual(result_b.location_repr(), "'e'")

        affected_code = (SourceRange.from_values('f'),
                         SourceRange.from_values('g'))
        result_c = Result('o', 'm', affected_code=affected_code)
        self.assertEqual(result_c.location_repr(), "'f', 'g'")

        affected_code = (SourceRange.from_values('f'),
                         SourceRange.from_values('f'))
        result_d = Result('o', 'm', affected_code=affected_code)
        self.assertEqual(result_d.location_repr(), "'f'")

    def test_json_diff(self):
        file_dict = {
            'f_a': ['1', '2', '3'],
            'f_b': ['1', '2', '3']
        }
        diff = Diff(file_dict['f_a'])
        diff.delete_line(2)
        diff.change_line(3, '3', '3_changed')
        uut = Result('origin', 'msg', diffs={'f_a': diff}).__json__(True)
        self.assertEqual(uut['diffs']['f_a'].__json__(), '--- \n'
                                                         '+++ \n'
                                                         '@@ -1,3 +1,2 @@\n'
                                                         ' 1-2-3+3_changed')
        JSONEncoder = create_json_encoder(use_relpath=True)
        json_dump = json.dumps(diff, cls=JSONEncoder, sort_keys=True)
        self.assertEqual(
            json_dump, '"--- \\n+++ \\n@@ -1,3 +1,2 @@\\n 1-2-3+3_changed"')
