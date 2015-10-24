import sys
import unittest

sys.path.insert(0, ".")
from coalib.results.Result import Result, RESULT_SEVERITY
from coalib.results.Diff import Diff


class ResultTest(unittest.TestCase):
    def test_origin(self):
        uut = Result("origin", "msg")
        self.assertEqual(uut.origin, "origin")

        uut = Result(self, "msg")
        self.assertEqual(uut.origin, "ResultTest")

        uut = Result(None, "msg")
        self.assertEqual(uut.origin, "")

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
                                  "file": "file",
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
        diff = Diff()
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

        diff = Diff()
        diff.delete_line(2)
        uut1 = Result("origin", "msg", diffs={"f_a": diff})

        diff = Diff()
        diff.change_line(3, "3", "3_changed")
        uut2 = Result("origin", "msg", diffs={"f_a": diff})

        diff = Diff()
        diff.change_line(3, "3", "3_changed")
        uut3 = Result("origin", "msg", diffs={"f_b": diff})

        uut1 += uut2 + uut3
        uut1.apply(file_dict)

        self.assertEqual(file_dict, expected_file_dict)


if __name__ == '__main__':
    unittest.main(verbosity=2)
