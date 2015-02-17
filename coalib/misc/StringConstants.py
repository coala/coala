import inspect
import os

from coalib.misc.i18n import _


class StringConstants:
    THIS_IS_A_BUG = _("This is a bug. We are sorry for the inconvenience. "
                      "Please contact the developers for assistance.")

    OBJ_NOT_ACCESSIBLE = _("{} is not accessible and will be ignored!")

    TRUE_STRINGS = ['1',
                    "on",
                    'y',
                    'yes',
                    "yeah",
                    "sure",
                    'true',
                    'definitely',
                    'yup',
                    "right"]

    FALSE_STRINGS = ['0',
                     'off',
                     'n',
                     'no',
                     'nope',
                     'nah',
                     'false',
                     "wrong"]

    # This string contains many unicode characters and is intended to challenge tests.
    COMPLEX_TEST_STRING = "4 r34l ch4ll3n63: 123 ÄÖü ABc @€¥ §&% {[( ←↓→↑ ĦŊħ ß°^ \\\n\u2192"

    # This is the directory where results from coverage for unittests are stored.
    COVERAGE_DIR = "./.coverageresults"

    # Path to the coalib directory
    coalib_root = os.path.join(os.path.dirname(inspect.getfile(_)), os.path.pardir)

    # Path to the directory containing the default bears
    coalib_bears_root = os.path.join(coalib_root, os.path.pardir, "bears")
