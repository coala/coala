import unittest
import sys

sys.path.insert(0, ".")
from bears.python.PyImportSortBear import PyImportSortBear
from bears.tests.LocalBearTestHelper import generate_local_bear_test


PyImportSortBearTest = generate_local_bear_test(
    PyImportSortBear,
    (["import os\n",
      "import sys\n"],),
    (["import sys\n",
      "import os\n"],))


if __name__ == '__main__':
    unittest.main(verbosity=2)
