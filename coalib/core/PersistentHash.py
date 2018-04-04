from collections import Iterable
from copy import deepcopy
from hashlib import sha1
import pickle


def order(obj):
    """
    Recursively preserves the order of any sets or dicts
    found in obj.
    """
    if isinstance(obj, set):
        return sorted(obj)
    if isinstance(obj, dict):
        temp_obj = deepcopy(obj)
        for k, v in temp_obj.items():
            if isinstance(v, set) or isinstance(v, dict):
                temp_obj[k] = order(v)
        return sorted(temp_obj.items())
    return obj


def preserve_order(a, k):
    arg_list = []
    for ele in a:
        arg_list.append(order(ele))

    kwargs = sorted(({key: order(value) for key, value in k.items()}).items())
    return tuple(arg_list), kwargs


def persistent_hash(obj):
    if isinstance(obj, Iterable):
        if isinstance(obj, dict):
            obj = sorted(obj.items())
        if isinstance(obj, set):
            obj = sorted(obj)
        # Specific condition for identifying task objects
        if (isinstance(obj[0], set) or isinstance(obj[1], dict)):
            obj = preserve_order(obj[0], obj[1])

    fingerprint_generator = sha1()
    fingerprint_generator.update(pickle.dumps(obj, protocol=4))
    return fingerprint_generator.digest()
