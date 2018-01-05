#!/usr/bin/env python3
"""
generate_dictionary.py

Generates custom documentation dictionary for SpellCheckBear
"""

import os
import sys
import shutil

import appdirs
from scspell import __file__ as scfile


class GenerateDictAction:
    """Represents the action of generating a new dictionary based on a
    custom dictionary."""
    if sys.platform == "win32":
        USER_DATA_DIR = appdirs.user_data_dir(
            appname='scspell', appauthor=False, roaming=True)
    else:
        USER_DATA_DIR = os.path.join(os.path.expanduser('~'), '.scspell')
    DICT_DEFAULT_LOC = os.path.join(USER_DATA_DIR, 'dictionary.txt')
    SCSPELL_DATA_DIR = os.path.normpath(
        os.path.join(os.path.dirname(scfile), 'data'))
    SCSPELL_BUILTIN_DICT = os.path.join(SCSPELL_DATA_DIR, 'dictionary.txt')
    CUSTOM_DICT = os.path.join(os.path.dirname(__file__), 'dictionary.txt')

    def run(self):
        try:
            os.mkdir(self.USER_DATA_DIR) if not os.path.exists(
                self.USER_DATA_DIR) else 0
            shutil.copy(self.SCSPELL_BUILTIN_DICT, self.DICT_DEFAULT_LOC)
            with open(self.DICT_DEFAULT_LOC, 'a') as output_dict:
                with open(self.CUSTOM_DICT, 'r') as input_dict:
                    for line in input_dict:
                        output_dict.write(line)
        except IOError or OSError:
            print('Could not copy the dictionary to its default location.\n'
                  'Check file permissions and try again.')
            sys.exit(1)


if __name__ == '__main__':
    GenerateDictAction().run()
