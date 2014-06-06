__author__ = 'lasse'

from enum import Enum


class CONSOLE_COLOR(Enum):
    invalid = 0
    normal = '0'
    black = '0;30'
    bright_gray = '0;37'
    blue = '0;34'
    white = '1;37'
    green = '0;32'
    bright_blue = '1;34',
    cyan = '0;36'
    bright_green = '1;32'
    red = '0;31'
    bright_cyan = '1;36'
    purple = '0;35'
    bright_red = '1;31',
    yellow = '0;33'
    bright_purple = '1;35',
    dark_gray = '1;30'
    bright_yellow = '1;33',
    # TODO is that all?

    @staticmethod
    def from_string(string):
        try:
            return CONSOLE_COLOR[string.replace(' ', '_').lower()]
        except KeyError:
            return CONSOLE_COLOR.invalid
