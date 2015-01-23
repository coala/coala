import sys

sys.path.insert(0, ".")
from coalib.results.LineResult import Result, LineResult
import unittest


class ResultTestCase(unittest.TestCase):
    def setUp(self):
        self.uut = LineResult("origin", 1, "line", "message", "file")

    def test_equality(self):
        cmp = LineResult("origin", 1, "line", "message", "file")
        self.assertEqual(cmp, self.uut)
        cmp = Result("origin", "message")
        self.assertNotEqual(cmp, self.uut)
        cmp = LineResult("origin", 1, "lineswrong", "message", "file")
        self.assertNotEqual(cmp, self.uut)

    def test_str_conversion(self):
        self.assertEqual(self.uut.__str__(), """LineResult:
 origin: 'origin'
 file: 'file'
 severity: 1
 line: 'line'
 line nr: 1
'message'""")


if __name__ == '__main__':
    unittest.main(verbosity=2)
