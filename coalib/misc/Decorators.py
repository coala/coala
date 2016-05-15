import inspect
from functools import total_ordering


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


def get_public_members(obj):
    """
    Retrieves a dictionary of member-like objects (members or properties) that
    are publicly exposed.

    :param obj: The object to probe.
    :return:    A dictionary with objects as keys and its attributes as values.
    """
    return {attr: getattr(obj, attr) for attr in dir(obj)
            if not attr.startswith("_")
            and not hasattr(getattr(obj, attr), '__call__')}


def generate_repr(*members):
    """
    Decorator that binds an auto-generated ``__repr__()`` function to a class.

    The generated ``__repr__()`` function prints in following format:
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
                            built-in ``repr()``). Using None as representation
                            function is the same as using ``repr()``.

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
            members_to_print = get_public_members(self)

            member_repr_list = ((member, repr) for member in
                                sorted(members_to_print, key=str.lower))

            return _construct_repr_string(self, member_repr_list)

    return decorator


def generate_eq(*members):
    """
    Decorator that generates equality and inequality operators for the
    decorated class. The given members as well as the type of self and other
    will be taken into account.

    Note that this decorator modifies the given class in place!

    :param members: A list of members to compare for equality.
    """
    def decorator(cls):
        def eq(self, other):
            if type(other) is not type(self):
                return False

            return all(getattr(self, member) == getattr(other, member)
                       for member in members)

        def ne(self, other):
            return not eq(self, other)

        cls.__eq__ = eq
        cls.__ne__ = ne
        return cls

    return decorator


def generate_ordering(*members):
    """
    Decorator that generates ordering operators for the decorated class based
    on the given member names. All ordering except equality functions will
    raise a TypeError when a comparison with an unrelated class is attempted.
    (Comparisons with child classes will thus work fine with the capabilities
    of the base class as python will choose the base classes comparison
    operator in that case.)

    Note that this decorator modifies the given class in place!

    :param members: A list of members to compare, ordered from high priority to
                    low. I.e. if the first member is equal the second will be
                    taken for comparison and so on. If a member is None it is
                    considered smaller than any other value except None.
    """
    def decorator(cls):
        def lt(self, other):
            if not isinstance(other, cls):
                raise TypeError("Comparison with unrelated classes is "
                                "unsupported.")

            for member in members:
                if getattr(self, member) == getattr(other, member):
                    continue

                if (
                        getattr(self, member) is None or
                        getattr(other, member) is None):
                    return getattr(self, member) is None

                return getattr(self, member) < getattr(other, member)

            return False

        cls.__lt__ = lt
        return total_ordering(generate_eq(*members)(cls))

    return decorator


def assert_right_type(value, types, argname):
    if isinstance(types, type) or types is None:
        types = (types,)

    for typ in types:
        if value == typ or (isinstance(typ, type) and isinstance(value, typ)):
            return

    raise TypeError("{} must be an instance of one of {} (provided value: "
                    "{!r})".format(argname, types, value))


def enforce_signature(function):
    """
    Enforces the signature of the function by throwing TypeError's if invalid
    arguments are provided. The return value is not checked.

    You can annotate any parameter of your function with the desired type or a
    tuple of allowed types. If you annotate the function with a value, this
    value only will be allowed (useful especially for None). Example:

    >>> @enforce_signature
    ... def test(arg: bool, another: (int, None)):
    ...     pass
    ...
    >>> test(True, 5)
    >>> test(True, None)

    Any string value for any parameter e.g. would then trigger a TypeError.

    :param function: The function to check.
    """
    argspec = inspect.getfullargspec(function)
    annotations = argspec.annotations
    argnames = argspec.args

    unnamed_annotations = {}
    for i, arg in enumerate(argnames):
        if arg in annotations:
            unnamed_annotations[i] = (annotations[arg], arg)

    def decorated(*args, **kwargs):
        for i, annotation in unnamed_annotations.items():
            if i < len(args):
                assert_right_type(args[i], annotation[0], annotation[1])

        for argname, argval in kwargs.items():
            if argname in annotations:
                assert_right_type(argval, annotations[argname], argname)

        return function(*args, **kwargs)

    return decorated


class classproperty(property):
    """
    Decorator to set a class function to a class property.

    Given a class like:

    >>> class test:
    ...     @classproperty
    ...     def func(self):
    ...         return 1

    We can now access the class property using the class name:

    >>> test.func
    1

    And we can still have the same behaviour with an instance:

    >>> test().func
    1
    """

    def __get__(self, obj, type_):
        return self.fget.__get__(None, type_)(type_)
