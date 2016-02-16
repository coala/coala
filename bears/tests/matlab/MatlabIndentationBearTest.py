from bears.matlab.MatlabIndentationBear import MatlabIndentationBear
from bears.tests.LocalBearTestHelper import verify_local_bear

MatlabIndentationBearTest = verify_local_bear(
    MatlabIndentationBear,
    valid_files=(["if a ~= b\n", "  a\n", "endif\n"],
                 ("if a ~= b\n", "  a\n", "endif\n"),
                 ["if a ~= b\n",
                  "  a\n",
                  "  \n",
                  "else\n",
                  "  a\n",
                  "endif\n"]),
    invalid_files=(["  A"],
                   ["if a ~= b\n", "a\n", "endif\n"],
                   ["if a ~= b\n", " a\n", "endif\n"],
                   ("if a ~= b\n", " a\n", "endif\n"),
                   ["if a ~= b\n",
                    "  a\n",
                    "  else\n",
                    "  a\n",
                    "endif\n"]))
