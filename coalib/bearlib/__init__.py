"""
The bearlib is an optional library designed to ease the task of any Bear. Just
as the rest of coala the bearlib is designed to be as easy to use as possible
while offering the best possible flexibility.
"""

import logging

from coalib.settings.FunctionMetadata import FunctionMetadata


def deprecate_settings(**depr_args):
    """
    The purpose of this decorator is to allow passing old settings names to
    bears due to the heavy changes in their names.

    >>> @deprecate_settings(new='old')
    ... def run(new):
    ...     print(new)

    Now we can simply call the bear with the deprecated setting, we'll get a
    warning - but it still works!

    >>> import sys
    >>> logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    >>> run(old="Hello world!")
    WARNING:root:The setting `old` is deprecated. Please use `new` instead.
    Hello world!
    >>> run(new="Hello world!")
    Hello world!

    This example represents the case where the old setting name needs to be
    modified to match the new one.

    >>> @deprecate_settings(new=('old', lambda a: a + 'coala!'))
    ... def func(new):
    ...     print(new)

    >>> func(old="Welcome to ")
    WARNING:root:The setting `old` is deprecated. Please use `new` instead.
    Welcome to coala!
    >>> func(new='coala!')
    coala!

    This example represents the case where the old and new settings are
    provided to the function.

    >>> @deprecate_settings(new='old')
    ... def run(new):
    ...     print(new)
    >>> # doctest: +ELLIPSIS
    ... run(old="Hello!", new='coala is always written with lowercase `c`.')
    WARNING:root:The setting `old` is deprecated. Please use `new` instead.
    WARNING:root:The value of `old` and `new` are conflicting. `new` will...
    coala is always written with lowercase `c`.
    >>> run(old='Hello!', new='Hello!')
    WARNING:root:The setting `old` is deprecated. Please use `new` instead.
    Hello!

    The metadata for coala has been adjusted as well:

    >>> list(run.__metadata__.non_optional_params.keys())
    ['new']
    >>> list(run.__metadata__.optional_params.keys())
    ['old']

    You cannot deprecate an already deprecated setting. Don't try. It will
    introduce non-deterministic errors in your program.

    :param depr_args: A dictionary of settings as keys and their deprecated
                      names as values.
    """
    def _deprecate_decorator(func):

        def wrapping_function(*args, **kwargs):
            for arg, depr_arg_and_modifier in depr_args.items():
                deprecated_arg, _func = (
                    depr_arg_and_modifier
                    if isinstance(depr_arg_and_modifier, tuple)
                    else (depr_arg_and_modifier, lambda x: x))
                if deprecated_arg in kwargs:
                    logging.warning(
                        'The setting `{}` is deprecated. Please use `{}` '
                        'instead.'.format(deprecated_arg, arg))
                    depr_arg_value = _func.__call__(kwargs[deprecated_arg])
                    if arg in kwargs and depr_arg_value != kwargs[arg]:
                        logging.warning(
                            'The value of `{}` and `{}` are conflicting.'
                            ' `{}` will be used instead.'.format(
                                  deprecated_arg, arg, arg))
                    else:
                        kwargs[arg] = depr_arg_value
                    del kwargs[deprecated_arg]
            return func(*args, **kwargs)

        new_metadata = FunctionMetadata.from_function(func)
        for arg, depr_arg_and_modifier in depr_args.items():
            deprecated_arg = (depr_arg_and_modifier[0]
                              if isinstance(depr_arg_and_modifier, tuple)
                              else depr_arg_and_modifier)
            new_metadata.add_deprecated_param(arg, deprecated_arg)
        wrapping_function.__metadata__ = new_metadata

        return wrapping_function

    return _deprecate_decorator


def deprecate_bear(bear):
    """
    Use this to deprecate a bear. Say we have a bear:

    >>> class SomeBear:
    ...     def run(*args):
    ...         print("I'm running!")

    To change the name from ``SomeOldBear`` to ``SomeBear`` you can keep the
    ``SomeOldBear.py`` around with those contents:

    >>> @deprecate_bear
    ... class SomeOldBear(SomeBear): pass

    Now let's run the bear:

    >>> import sys
    >>> logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    >>> SomeOldBear().run()
    WARNING:root:The bear SomeOldBear is deprecated. Use SomeBear instead!
    I'm running!

    :param bear: An old bear class that inherits from the new one (so it gets
                 its methods and can just contain a pass.)
    :return: A bear class that warns about deprecation on use.
    """
    bear.old_run = bear.run

    def warn_deprecation_and_run(*args, **kwargs):
        logging.warning('The bear {} is deprecated. Use {} instead!'.format(
            bear.__name__, bear.__bases__[0].__name__
        ))
        return bear.old_run(*args, **kwargs)

    bear.run = warn_deprecation_and_run
    return bear
