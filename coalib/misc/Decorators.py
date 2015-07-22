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


def generate_repr(*members):
    """
    Decorator that binds an auto-generated `__repr__()` function to a class.

    The generated `__repr__()` function prints in following format:
    <ClassName object(field1=1, field2='A string', field3=[1, 2, 3]) at 0xAAAA>

    Note that this decorator modifies the given class in place!

    :param members:     An iterable of member names to include into the
                        representation-string. Providing no members yields to
                        inclusion of all available members.

                        To control the representation of each member, you can
                        also pass a tuple where the first element contains the
                        member to print and the second one the representation
                        function (which defaults to the built-in `repr()`).
                        Using None as representation function is the same as
                        using `repr()`.
                        I.e. passing `"memberA", "memberB", ("memberC", str)`
                        would be the same as supplying
                        ```
                        ("memberA", repr), ("memberB", repr), ("memberC", str)
                        ```

                        If you want to print members that aren't actually
                        fields (i.e. properties), you can use a third tuple
                        field. It determines whether members shall searched
                        or not. Also it feeds the given lambda not with the
                        member value, but with the class instance (self).
                        For example if you want to display a property, you
                        pass to this parameter:
                        `("property-A", lambda self: self.get_A(), True)`
                        Using `True` in the third tuple entry enables this
                        behaviour. Using False disables it and behaves like
                        the simpler constructs above.
    :raises ValueError: Raised when the passed
                        (member, repr-function, manual-get)-tuples have not a
                        length of 2 or 3.
    :return:            The class armed with an auto-generated __repr__
                        function.
    """
    def construct_repr_string(self, members):
        # The passed entries have format (member-name, repr-function).
        values = ", ".join(member + "=" +
                           (func(self) if manual_get else
                            func(self.__dict__[member]))
                           for member, func, manual_get in members)
        return ("<" + self.__class__.__name__ + " object(" + values +
                ") at " + hex(id(self)) + ">")

    if members:
        # Prepare members list.
        members_to_print = list(members)
        for i, member in enumerate(members_to_print):
            if isinstance(member, tuple):
                # Check tuple dimensions.
                length = len(member)
                if length == 2:
                    members_to_print[i] = (member[0],
                                           member[1] if member[1] else repr,
                                           False)
                elif length == 3:
                    members_to_print[i] = (member[0],
                                           member[1] if member[1] else repr,
                                           member[2])
                else:
                    raise ValueError("Passed tuple " + repr(member) +
                                     " needs to be 2- or 3-dimensional, but "
                                     "has " + str(length) + " dimensions.")
            else:
                members_to_print[i] = (member, repr, False)

        def __repr__(self):
            return construct_repr_string(self, members_to_print)
    else:
        def __repr__(self):
            # Need to fetch members every time since they are unknown until
            # class instantation.
            members_to_print = (
                (member, repr, False) for member in self.__dict__)
            return construct_repr_string(self, members_to_print)

    def decorator(cls):
        cls.__repr__ = __repr__
        return cls

    return decorator
