import os

from coalib.misc.i18n import _


class Constants:
    THIS_IS_A_BUG = _("This is a bug. We are sorry for the inconvenience. "
                      "Please contact the developers for assistance.")

    CRASH_MESSAGE = _("An unknown error occurred. This is a bug. We are "
                      "sorry for the inconvenience. Please contact the "
                      "developers for assistance. During execution of "
                      "coala an exception was raised. This should never "
                      "happen. When asked for, the following information "
                      "may help investigating:")

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

    # This string contains many unicode characters to challenge tests.
    COMPLEX_TEST_STRING = ("4 r34l ch4ll3n63: 123 ÄÖü ABc @€¥ §&% {[( ←↓→↑ "
                           "ĦŊħ ß°^ \\\n\u2192")

    # Results from coverage for unittests are stored here.
    COVERAGE_DIR = "./.coverageresults"

    # Path to the coalib directory
    coalib_root = os.path.join(os.path.dirname(__file__),
                               os.path.pardir)

    # Path to the directory containing the default bears
    coalib_bears_root = os.path.join(coalib_root, os.path.pardir, "bears")

    # Path to the language definition files
    language_definitions = os.path.join(coalib_root,
                                        "bearlib",
                                        "languages",
                                        "definitions")

    system_coafile = os.path.join(coalib_root, "default_coafile")

    user_coafile = os.path.join(os.path.expanduser("~"), ".coarc")

    VERSION_FILE = os.path.join(coalib_root, "VERSION")
    with open(VERSION_FILE, 'r') as ver:
        VERSION = ver.readline().strip()

    BUS_NAME = "org.coala_analyzer.v1"
