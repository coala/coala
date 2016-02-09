import unittest

from bears.python.PyImportSortBear import PyImportSortBear
from bears.tests.LocalBearTestHelper import verify_local_bear


PyImportSortBearTest = verify_local_bear(PyImportSortBear,
                                         (["import os\n", "import sys\n"],),
                                         (["import sys\n", "import os\n"],))


if __name__ == '__main__':
    unittest.main(verbosity=2)
