from collections import Iterable, OrderedDict


def inverse_dicts(*dicts):
    """
    Inverts the dicts, e.g. {1: 2, 3: 4} and {2: 3, 4: 4} will be inverted
    {2: [1], 3: [2], 4: [3, 4]}. This also handles dictionaries
    with Iterable items as values e.g. {1: [1, 2, 3], 2: [3, 4, 5]} and
    {2: [1], 3: [2], 4: [3, 4]} will be inverted to
    {1: [1, 2], 2: [1, 3], 3: [1, 2, 4], 4: [2, 4], 5: [2]}.
    No order is preserved.

    :param dicts: The dictionaries to invert.
    :return:      The inversed dictionary which merges all dictionaries into
                  one.
    """
    inverse = {}

    for dictionary in dicts:
        for key, value in dictionary.items():
            if isinstance(value, Iterable):
                for item in value:
                    add_pair_to_dict(item, key, inverse)
            else:
                add_pair_to_dict(value, key, inverse)

    return inverse


def add_pair_to_dict(key, value, dictionary):
    """
    Add (key, value) pair to the dictionary. The value is added to a list of
    values for the key.
    """
    if key in dictionary:
        dictionary[key].append(value)
    else:
        dictionary[key] = [value]


def update_ordered_dict_key(dictionary, old_key, new_key):
    return OrderedDict(((new_key if k == old_key else k), v)
                       for k, v in dictionary.items())
