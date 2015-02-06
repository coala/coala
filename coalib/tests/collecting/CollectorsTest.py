import inspect
import os
import sys

import unittest

sys.path.insert(0, ".")
from coalib.collecting.Collectors import collect_files


class ImportObjectsTestCase(unittest.TestCase):

    def setUp(self):
        current_dir = os.path.split(inspect.getfile(inspect.currentframe()))[0]
        self.collectors_test_dir = os.path.join(current_dir, "collectors_test_dir")

    def test_empty(self):
        self.assertRaises(TypeError, collect_files)

    def test_invalid(self):
        self.assertEqual(collect_files(["invalid_path"]), [])

    def test_collection(self):
        self.assertEqual(collect_files([os.path.join(self.collectors_test_dir, "others", "*", "*2.py")]), [os.path.join(self.collectors_test_dir, "others", "py_files", "file2.py")])



if __name__ == '__main__':
    unittest.main(verbosity=2)
