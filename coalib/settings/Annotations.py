def typechain(*args):
    """
    Returns function which applies the first transformation it can from args
    and returns transformed value, or the value itself if it is in args.

    >>> function = typechain(int, 'a', ord, None)
    >>> function("10")
    10
    >>> function("b")
    98
    >>> function("a")
    'a'
    >>> function(int)
    <class 'int'>
    >>> function(None) is None
    True
    >>> function("str")
    Traceback (most recent call last):
        ...
    ValueError: Couldn't convert value 'str' to any specified type or find it \
in specified values.

    :raises TypeError:  Raises when either no functions are specified for
                        checking.
    """
    if len(args) == 0:
        raise TypeError('No arguments were provided.')

    def annotation(value):
        """
        Returns value either transformed with one of the function in args, or
        casted to one of types in args, or the value itself if it is in the
        args.

        :raises ValueError: Raises when cannot transform value in any one of
                            specified ways.
        """
        for arg in args:
            if value == arg:
                return value
            if isinstance(arg, type) and isinstance(value, arg):
                return value
            try:
                return arg(value)
            except (ValueError, TypeError):
                pass
        raise ValueError(
            "Couldn't convert value {!r} to any specified type "
            'or find it in specified values.'.format(value))
    return annotation
