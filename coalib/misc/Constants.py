# -*- coding: utf-8 -*-

import os
import appdirs

THIS_IS_A_BUG = ("This is a bug. We are sorry for the inconvenience. "
                 "Please contact the developers for assistance.")

CRASH_MESSAGE = ("An unknown error occurred. This is a bug. We are "
                 "sorry for the inconvenience. Please contact the "
                 "developers for assistance. During execution of "
                 "coala an exception was raised. This should never "
                 "happen. When asked for, the following information "
                 "may help investigating:")

VERSION_CONFLICT_MESSAGE = ("There is a conflict in the version of a "
                            "dependency you have installed and the "
                            "requirements of coala. This may be resolved by "
                            "creating a separate virtual environment for "
                            "coala or running `pip install %s`. Be aware "
                            "that the latter solution might break other "
                            "python packages that depend on the currently "
                            "installed version.")

OBJ_NOT_ACCESSIBLE = "{} is not accessible and will be ignored!"

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

# Path to the coalib directory
coalib_root = os.path.join(os.path.dirname(__file__),
                           os.path.pardir)

# Path to the language definition files
language_definitions = os.path.join(coalib_root,
                                    "bearlib",
                                    "languages",
                                    "definitions")

system_coafile = os.path.join(coalib_root, "default_coafile")

user_coafile = os.path.join(os.path.expanduser("~"), ".coarc")

default_coafile = ".coafile"

VERSION_FILE = os.path.join(coalib_root, "VERSION")
with open(VERSION_FILE, 'r') as ver:
    VERSION = ver.readline().strip()

BUS_NAME = "org.coala_analyzer.v1"

TAGS_DIR = appdirs.user_data_dir('coala', version=VERSION)

GLOBBING_SPECIAL_CHARS = "()[]|?*"
