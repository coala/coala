def yield_once(iterator):
    """
    Decorator to make an iterator yield each result only once.

    :param iterator: Any iterator
    :return:         An iterator that yields every result only once at most.
    """
    def yield_once_generator(*args, **kwargs):
        yielded = []
        for item in iterator(*args, **kwargs):
            if item in yielded:
                pass
            else:
                yielded.append(item)
                yield item

    return yield_once_generator


def _to_list(var):
    """
    Make variable to list.

    :param var: variable of any type
    :return:    list
    """
    if isinstance(var, list):
        return var
    elif var is None:
        return []
    elif isinstance(var, str) or isinstance(var, dict):
        # We dont want to make a list out of those via the default constructor
        return [var]
    else:
        try:
            return list(var)
        except TypeError:
            return [var]


def arguments_to_lists(function):
    """
    Decorator for a function that converts all arguments to lists.

    :param function: target function
    :return:         target function with only lists as parameters
    """
    def l_function(*args, **kwargs):
        l_args = [_to_list(arg) for arg in args]
        l_kwargs = {}

        for key, value in kwargs.items():
            l_kwargs[key] = _to_list(value)
        return function(*l_args, **l_kwargs)

    return l_function
