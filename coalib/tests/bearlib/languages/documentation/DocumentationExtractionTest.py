import unittest
import sys

sys.path.insert(0, ".")
from coalib.bearlib.languages.documentation.DocumentationExtraction import (
    extract_documentation)
from coalib.misc.Compatability import FileNotFoundError


class DocumentationExtractionTest(unittest.TestCase):
    def test_extract_documentation_invalid_input(self):
        with self.assertRaises(FileNotFoundError):
            tuple(extract_documentation("", "PYTHON", "INVALID"))


if __name__ == '__main__':
    unittest.main(verbosity=2)
