import sys
import unittest

sys.path.insert(0, ".")
from bears.tests.LocalBearTestHelper import generate_local_bear_test
from bears.matlab.MatlabIndentationBear import MatlabIndentationBear


MatlabIndentationBearTest = generate_local_bear_test(
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
