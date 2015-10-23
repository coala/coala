import re
import sys
import unittest

sys.path.insert(0, ".")
from coalib.parsing.StringProcessing import trim_empty


class TestClass:
    def __init__(self, value):
        self.value = value

    def __len__(self):
        return self.value


class TrimEmptyTest(unittest.TestCase):
    def test_strings(self):
        testsequence = ("abc", "", "", "def", "1", "", "ghijklmn", "", "")
        self.assertEqual(tuple(trim_empty(testsequence)),
                         ("abc", "def", "1", "ghijklmn"))

        testsequence = tuple()
        self.assertEqual(tuple(trim_empty(testsequence)), tuple())

        testsequence = ("", "", "", "")
        self.assertEqual(tuple(trim_empty(testsequence)), tuple())

    def test_custom_class(self):
        testsequence = (TestClass(0),
                        TestClass(12),
                        TestClass(24),
                        TestClass(0),
                        TestClass(9),
                        TestClass(0))
        self.assertEqual(tuple(x.value for x in trim_empty(testsequence)),
                         (12, 24, 9))

        testsequence = (TestClass(0),
                        TestClass(0),
                        TestClass(177))
        self.assertEqual(tuple(x.value for x in trim_empty(testsequence)),
                         (177,))


if __name__ == '__main__':
    unittest.main(verbosity=2)
