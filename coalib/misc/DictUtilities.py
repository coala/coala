from collections import Iterable

def inverse_dicts(*dicts):
    """
    Inverts the dicts, e.g. {1: 2, 3: 4} and {2: 3, 4: 4} will be inverted
    {2: [1, 2], 4: [3, 4]}. No order is preserved.

    :param dicts: The dictionaries to invert.
    :return:      TOWRITE
    """
    inverse = {}

    for dict in dicts:
        for key, value in dict.items():
            if isinstance(value, Iterable):
                for item in value:
                    if item in inverse:
                        inverse[item].append(key)
                    else:
                        inverse[item] = [key]
            else:
                if value in inverse:
                    inverse[value].append(key)
                else:
                    inverse[value] = [key]

    return inverse
