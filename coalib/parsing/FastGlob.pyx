import fnmatch
import os

from coalib.misc.Decorators import yield_once
from coalib.misc.i18n import N_

def _iter_or_combinations(str pattern,
                          str opening_delimiter="(",
                          str closing_delimiter=")",
                          str separator = "|"):
    cdef list yielded = []
    cdef str item
    for item in ioc(pattern, opening_delimiter, closing_delimiter, separator):
        if item in yielded:
            pass
        else:
            yielded.append(item)
            yield item

def ioc(str pattern,
        str opening_delimiter="(",
        str closing_delimiter=")",
        str separator="|"):

    # Taking the leftmost closing delimiter and the rightmost opening delimiter
    # left of it ensures that the delimiters belong together and the pattern is
    # parsed correctly from the most nested section outwards.
    cdef long closing_pos, opening_pos
    closing_pos = pattern.find(closing_delimiter)
    opening_pos = pattern[:closing_pos].rfind(opening_delimiter)

    if (
            (closing_pos == -1) != (opening_pos == -1) or
            # Special case that gets overlooked because opening_delimiter
            # is only being looked for in pattern[:-1] when closing_pos == -1
            (closing_pos == -1 and pattern.endswith(opening_delimiter))):
        raise ValueError(N_("Parentheses of pattern are not matching"))

    cdef str prefix, parenthesized, postfix, combination, new_combination, new_pattern, choice
    if -1 not in (opening_pos, closing_pos):
        prefix = pattern[:opening_pos]
        parenthesized = pattern[opening_pos+len(opening_delimiter):closing_pos]
        postfix = pattern[closing_pos+len(closing_delimiter):]
        # This loop iterates through all possible combinations that can be
        # inserted in place of the first innermost pair of parentheses:
        # "(a|b)(c|d)" yields "a", then "b"
        for combination in ioc(parenthesized,
                               opening_delimiter,
                               closing_delimiter,
                               separator):
            new_pattern = prefix + combination + postfix
            # This loop iterates through all possible combinations for the new
            # whole pattern, which has it's first pair of parentheses replaced
            # already:
            # "a(cd)" (first call) yields "ac", then "ad",
            # "b(cd)" (second call) yields "bc" and "bd"
            for new_combination in ioc(new_pattern,
                                       opening_delimiter,
                                       closing_delimiter,
                                       separator):
                yield new_combination
    elif separator in pattern:
        for choice in pattern.split(separator):
            yield choice
    else:
        yield pattern