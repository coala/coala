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


def _get_member(obj, member):
    # If not found, pass AttributeError to invoking function.
    attribute = getattr(obj, member)

    if callable(attribute) and hasattr(attribute, "__self__"):
        # If the value is a bound method, invoke it like a getter and return
        # its value.
        try:
            return attribute()
        except TypeError:
            # Don't use repr() to display the member more accurately, because
            # invoking repr() on a bound method prints in this format:
            # <bound method CLASS.METHOD of **repr(instance)**>
            # This invokes repr() recursively.
            raise TypeError("Given bound method '" + member + "' must be "
                            "callable like a getter, taking no arguments.")
    else:
        # Otherwise it's a member variable or property (or any other attribute
        # that holds a value).
        return attribute


def _construct_repr_string(obj, members):
    # The passed entries have format (member-name, repr-function).
    values = ", ".join(member + "=" + func(_get_member(obj, member))
                       for member, func in members)
    return ("<" + type(obj).__name__ + " object(" + values + ") at "
            + hex(id(obj)) + ">")


def generate_repr(*members):
    """
    Decorator that binds an auto-generated `__repr__()` function to a class.

    The generated `__repr__()` function prints in following format:
    <ClassName object(field1=1, field2='A string', field3=[1, 2, 3]) at 0xAAAA>

    Note that this decorator modifies the given class in place!

    :param members:         An iterable of member names to include into the
                            representation-string. Providing no members yields
                            to inclusion of all member variables and properties
                            in alphabetical order (except if they start with an
                            underscore).

                            To control the representation of each member, you
                            can also pass a tuple where the first element
                            contains the member to print and the second one the
                            representation function (which defaults to the
                            built-in `repr()`). Using None as representation
                            function is the same as using `repr()`.

                            Supported members are fields/variables, properties
                            and getter-like functions (functions that accept no
                            arguments).
    :raises ValueError:     Raised when the passed
                            (member, repr-function)-tuples have not a length of
                            2.
    :raises AttributeError: Raised when a given member/attribute was not found
                            in class.
    :raises TypeError:      Raised when a provided member is a bound method
                            that is not a getter-like function (means it must
                            accept no parameters).
    :return:                The class armed with an auto-generated __repr__
                            function.
    """
    def decorator(cls):
        cls.__repr__ = __repr__
        return cls

    if members:
        # Prepare members list.
        members_to_print = list(members)
        for i, member in enumerate(members_to_print):
            if isinstance(member, tuple):
                # Check tuple dimensions.
                length = len(member)
                if length == 2:
                    members_to_print[i] = (member[0],
                                           member[1] if member[1] else repr)
                else:
                    raise ValueError("Passed tuple " + repr(member) +
                                     " needs to be 2-dimensional, but has " +
                                     str(length) + " dimensions.")
            else:
                members_to_print[i] = (member, repr)

        def __repr__(self):
            return _construct_repr_string(self, members_to_print)
    else:
        def __repr__(self):
            # Need to fetch member variables every time since they are unknown
            # until class instantation.
            members_to_print = set(
                filter(lambda member: not member.startswith("_"),
                       self.__dict__))
            # Also fetch properties.
            self_type_dict = type(self).__dict__
            members_to_print |= set(
                filter(lambda member: isinstance(self_type_dict[member],
                                                 property)
                                      and not member.startswith("_"),
                       self_type_dict))

            member_repr_list = ((member, repr) for member in
                sorted(members_to_print, key=str.lower))

            return _construct_repr_string(self, member_repr_list)

    return decorator
