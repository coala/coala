from os.path import abspath
import unittest

from coalib.results.Result import Result, RESULT_SEVERITY
from coalib.results.Diff import Diff
from coalib.results.SourceRange import SourceRange


class ResultTest(unittest.TestCase):

    def test_origin(self):
        uut = Result("origin", "msg")
        self.assertEqual(uut.origin, "origin")

        uut = Result(self, "msg")
        self.assertEqual(uut.origin, "ResultTest")

        uut = Result(None, "msg")
        self.assertEqual(uut.origin, "")

    def test_invalid_severity(self):
        with self.assertRaises(ValueError):
            Result("o", "m", severity=-5)

    def test_string_dict(self):
        uut = Result(None, "")
        output = uut.to_string_dict()
        self.assertEqual(output, {"id": str(uut.id),
                                  "origin": "",
                                  "message": "",
                                  "file": "",
                                  "line_nr": "",
                                  "severity": "NORMAL",
                                  "debug_msg": ""})

        uut = Result.from_values(origin="origin",
                                 message="msg",
                                 file="file",
                                 line=2,
                                 severity=RESULT_SEVERITY.INFO,
                                 debug_msg="dbg")
        output = uut.to_string_dict()
        self.assertEqual(output, {"id": str(uut.id),
                                  "origin": "origin",
                                  "message": "msg",
                                  "file": abspath("file"),
                                  "line_nr": "2",
                                  "severity": "INFO",
                                  "debug_msg": "dbg"})

        uut = Result.from_values(origin="o", message="m", file="f", line=5)
        output = uut.to_string_dict()
        self.assertEqual(output["line_nr"], "5")

    def test_apply(self):
        file_dict = {
            "f_a": ["1", "2", "3"],
            "f_b": ["1", "2", "3"]
        }
        expected_file_dict = {
            "f_a": ["1", "3_changed"],
            "f_b": ["1", "2", "3"]
        }
        diff = Diff(file_dict['f_a'])
        diff.delete_line(2)
        diff.change_line(3, "3", "3_changed")

        uut = Result("origin", "msg", diffs={"f_a": diff})
        uut.apply(file_dict)

        self.assertEqual(file_dict, expected_file_dict)

    def test_add(self):
        file_dict = {
            "f_a": ["1", "2", "3"],
            "f_b": ["1", "2", "3"],
            "f_c": ["1", "2", "3"]
        }
        expected_file_dict = {
            "f_a": ["1", "3_changed"],
            "f_b": ["1", "2", "3_changed"],
            "f_c": ["1", "2", "3"]
        }

        diff = Diff(file_dict['f_a'])
        diff.delete_line(2)
        uut1 = Result("origin", "msg", diffs={"f_a": diff})

        diff = Diff(file_dict['f_a'])
        diff.change_line(3, "3", "3_changed")
        uut2 = Result("origin", "msg", diffs={"f_a": diff})

        diff = Diff(file_dict['f_b'])
        diff.change_line(3, "3", "3_changed")
        uut3 = Result("origin", "msg", diffs={"f_b": diff})

        uut1 += uut2 + uut3
        uut1.apply(file_dict)

        self.assertEqual(file_dict, expected_file_dict)

    def test_to_ignore(self):
        ranges = [([], SourceRange.from_values("f", 1, 1, 2, 2))]
        result = Result.from_values("origin",
                                    "message",
                                    file="e",
                                    line=1,
                                    column=1,
                                    end_line=2,
                                    end_column=2)

        self.assertFalse(result.to_ignore(ranges))

        ranges.append(([], SourceRange.from_values("e", 2, 3, 3, 3)))
        self.assertFalse(result.to_ignore(ranges))

        ranges.append(([], SourceRange.from_values("e", 1, 1, 2, 2)))
        self.assertTrue(result.to_ignore(ranges))

        result1 = Result.from_values("origin", "message", file="e")
        self.assertFalse(result1.to_ignore(ranges))

        ranges = [(['something', 'else', 'not origin'],
                   SourceRange.from_values("e", 1, 1, 2, 2))]
        self.assertFalse(result.to_ignore(ranges))

        ranges = [(['something', 'else', 'origin'],
                   SourceRange.from_values("e", 1, 1, 2, 2))]
        self.assertTrue(result.to_ignore(ranges))

    def test_location_repr(self):
        result_a = Result(origin="o", message="m")
        self.assertEqual(result_a.location_repr(), "the whole project")

        result_b = Result.from_values("o", "m", file="e")
        self.assertEqual(result_b.location_repr(), "'e'")

        affected_code = (SourceRange.from_values('f'),
                         SourceRange.from_values('g'))
        result_c = Result("o", "m", affected_code=affected_code)
        self.assertEqual(result_c.location_repr(), "'f', 'g'")

        affected_code = (SourceRange.from_values('f'),
                         SourceRange.from_values('f'))
        result_d = Result("o", "m", affected_code=affected_code)
        self.assertEqual(result_d.location_repr(), "'f'")


if __name__ == '__main__':
    unittest.main(verbosity=2)
