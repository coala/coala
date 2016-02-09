import unittest

from bears.tests.LocalBearTestHelper import verify_local_bear
from bears.matlab.MatlabIndentationBear import MatlabIndentationBear


MatlabIndentationBearTest = verify_local_bear(
    MatlabIndentationBear,
    valid_files=(["if a ~= b\n", "  a\n", "endif\n"],
                 ["if a ~= b\n",
                  "  a\n",
                  "  \n",
                  "else\n",
                  "  a\n",
                  "endif\n"]),
    invalid_files=(["  A"],
                   ["if a ~= b\n", "a\n", "endif\n"],
                   ["if a ~= b\n", " a\n", "endif\n"],
                   ["if a ~= b\n",
                    "  a\n",
                    "  else\n",
                    "  a\n",
                    "endif\n"]))


if __name__ == '__main__':
    unittest.main(verbosity=2)
