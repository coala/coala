"""
Filename matching with shell patterns.

Glob Syntax:
'[seq]':         Matches any character in seq. Cannot be empty.
                 Any Special Character looses its special meaning in a set.
'[!seq]':        Matches any character not in seq. Cannot be empty
                 Any Special Character looses its special meaning in a set.
'(seq_a|seq_b)': Matches either sequence_a or sequence_b as a whole.
                 More than two or just one sequence can be given.
'?':             Matches any single character.
'*':             Matches everything but os.sep.
'**':            Matches everything.
"""
import re

from coalib.misc.Decorators import yield_once


def _position_is_bracketed(string, position):
    """
    Tests whether the char at string[position] is inside a valid pair of
    brackets (and therefore looses its special meaning).
    """
    # allow negative positions and trim too long ones
    position = len(string[:position])

    index, length = 0, len(string)
    while index < position:
        char = string[index]
        index += 1
        if char == '[':
            closing_index = index
            if closing_index < length and string[closing_index] == '!':
                closing_index += 1
            if closing_index < length and string[closing_index] == ']':
                closing_index += 1
            while closing_index < length and string[closing_index] != ']':
                closing_index += 1
            if closing_index < length:
                if index <= position < closing_index:
                    return True
                index = closing_index + 1
    return False


def _iter_choices(pattern):
    """
    Iterate through each choice of an alternative.
    Basically splitting on '|'s if they are not bracketed
    """
    start_pos = 0
    split_pos_list = [match.start() for match in re.finditer('\\|', pattern)]
    split_pos_list.append(len(pattern))
    for end_pos in split_pos_list:
        if not _position_is_bracketed(pattern, end_pos):
            yield pattern[start_pos: end_pos]
            start_pos = end_pos + 1
