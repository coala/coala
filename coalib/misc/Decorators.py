def cached_iterator(iterator):
    """
    Decorator for an iterator that should not yield duplications
    :param iterator: python iterator
    :return: python iterator that yields each item only once per call
    """
    def c_iterator(*args, **kwargs):
        yielded = []
        for item in iterator(*args, **kwargs):
            if item in yielded:
                pass
            else:
                yielded.append(item)
                yield item
    return c_iterator


def _to_list(var):
    """
    make variable to list
    :param var: variable of any type
    :return: list
    """
    if isinstance(var, list):
        return var
    elif var is None:
        return []
    elif isinstance(var, str) or isinstance(var, dict):
        return [var]  # we can make a list out of this but be don't want to
    else:
        try:
            return list(var)
        except TypeError:
            return [var]


def arguments_to_lists(function):
    """
    Decorator for a function that converts all arguments to lists
    :param function: target function
    :return: target function with only lists as parameters
    """
    def l_function(*args, **kwargs):
        l_args = [_to_list(arg) for arg in args]
        l_kwargs = {}

        for key, value in kwargs.items():
            l_kwargs[key] = _to_list(value)
        return function(*l_args, **l_kwargs)

    return l_function