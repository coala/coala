__author__ = 'lasse'

from enum import Enum


class CONSOLE_COLOR(Enum):
    invalid=0
    normal= 1
    red =   2
    green = 3
    blue =  4
    # TODO more

    @staticmethod
    def from_string(string):
        try:
            return CONSOLE_COLOR[string.lower()]
        except KeyError:
            return CONSOLE_COLOR.invalid