import sys

sys.path.insert(0, ".")
from coalib.results.Result import Result, RESULT_SEVERITY
import unittest


class ResultTestCase(unittest.TestCase):
    def test_wrong_types(self):
        uut = Result('b', 'b')
        self.assertNotEqual(uut, 0)
        self.assertRaises(TypeError, uut.__ge__, 0)
        self.assertRaises(TypeError, uut.__le__, 0)
        self.assertRaises(TypeError, uut.__gt__, 0)
        self.assertRaises(TypeError, uut.__lt__, 0)

    def test_origin(self):
        uut = Result("origin", "msg")
        self.assertEqual(uut.origin, "origin")

        uut = Result(self, "msg")
        self.assertEqual(uut.origin, "ResultTestCase")

    def test_get_actions(self):
        self.assertEqual(len(Result("origin", "msg").get_actions()), 0)
        self.assertEqual(len(Result("origin", "msg", file="file").get_actions()), 1)

    def test_string_conversion(self):
        uut = Result('a', 'b', 'c')
        self.assertEqual(str(uut), "Result:\n origin: 'a'\n file: 'c'\n line nr: None\n severity: 1\n'b'")
        self.assertEqual(str(uut), repr(uut))
        self.assertEqual(Result("origin", "message", "file", line_nr=1).__str__(), """Result:
 origin: 'origin'
 file: 'file'
 line nr: 1
 severity: 1
'message'""")

    def test_ordering(self):
        """
        Tests the ordering routines of Result. This tests enough to have all branches covered. Not every case may be
        covered but I want to see the (wo)man who writes comparison routines that match these criteria and are wrong to
        the specification. (Given he does not engineer the routine to trick the test explicitly.)
        """
        medium = Result(origin='b', message='b', file='b', severity=RESULT_SEVERITY.NORMAL)
        medium_too = Result(origin='b', message='b', file='b', severity=RESULT_SEVERITY.NORMAL)
        self.assert_equal(medium, medium_too)

        bigger_file = Result(origin='b', message='b', file='c', severity=RESULT_SEVERITY.NORMAL)
        self.assert_ordering(bigger_file, medium)

        no_file = Result(origin='b', message='b', file=None, severity=RESULT_SEVERITY.NORMAL)
        self.assert_ordering(medium, no_file)

        no_file_and_unsevere = Result(origin='b', message='b', file=None, severity=RESULT_SEVERITY.INFO)
        self.assert_ordering(no_file_and_unsevere, no_file)
        self.assert_ordering(medium, no_file_and_unsevere)

        greater_origin = Result(origin='c', message='b', file='b', severity=RESULT_SEVERITY.NORMAL)
        self.assert_ordering(greater_origin, medium)

        medium.line_nr = 5
        greater_origin.line_nr = 3
        self.assert_ordering(medium, greater_origin)

        uut = Result("origin", "message", "file", line_nr=1)
        cmp = Result("origin", "message", "file", line_nr=1)
        self.assert_equal(cmp, uut)
        cmp = Result("origin", "message", "file")
        self.assertNotEqual(cmp, uut)

    def assert_equal(self, first, second):
        self.assertGreaterEqual(first, second)
        self.assertEqual(first, second)
        self.assertLessEqual(first, second)

    def assert_ordering(self, greater, lesser):
        self.assertGreater(greater, lesser)
        self.assertGreaterEqual(greater, lesser)
        self.assertNotEqual(greater, lesser)
        self.assertLessEqual(lesser, greater)
        self.assertLess(lesser, greater)


if __name__ == '__main__':
    unittest.main(verbosity=2)
