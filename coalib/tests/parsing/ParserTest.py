import sys

sys.path.insert(0, ".")
from coalib.parsing.SectionParser import SectionParser
import unittest


class ParserTest(unittest.TestCase):
    def test_parse_available(self):
        self.uut = SectionParser()
        self.assertRaises(NotImplementedError, self.uut.parse, None)

    def test_reparse_available(self):
        self.uut = SectionParser()
        self.assertRaises(NotImplementedError, self.uut.reparse, None)

    def test_export_available(self):
        self.uut = SectionParser()
        self.assertRaises(NotImplementedError, self.uut.export_to_settings)


if __name__ == '__main__':
    unittest.main(verbosity=2)
