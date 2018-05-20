"""
The bearlib is an optional library designed to ease the task of any Bear. Just
as the rest of coala the bearlib is designed to be as easy to use as possible
while offering the best possible flexibility.
"""

import logging
from functools import wraps

import pdb
from coalib.settings.FunctionMetadata import FunctionMetadata

db = pdb.Pdb()
db.prompt = '(coala-debugger)'
def _do_nothing(x): return x


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
    >>> # doctest:
    ... run(old="Hello!", new='coala is always written with lowercase `c`.')
    WARNING:root:The setting `old` is deprecated. Please use `new` instead.
    WARNING:root:The value of `old` and `new` are conflicting. `new` will...
    coala is always written with lowercase `c`.
    >>> @deprecate_settings(new='old')
    ... def run(new):
    ...     print(new)
    >>> run(old='Hello!', new='Hello!')
    WARNING:root:The setting `old` is deprecated. Please use `new` instead.
    Hello!

    Note that messages are cached. So the same message won't be printed twice:
    >>> run(old='Hello!', new='Hello!')
    Hello!

    Multiple deprecations can be provided for the same setting. The modifier
    function for each deprecated setting can be given as a value in a dict
    where the deprecated setting is the key. A default modifier may be
    specified at the end of the deprecated settings tuple.

    >>> @deprecate_settings(new=({'old': lambda x: x + ' coala!'},
    ...                          'older',
    ...                           lambda x: x + '!' ))
    ... def run(new):
    ...     print(new)
    >>> run(old='Hi')
    WARNING:root:The setting `old` is deprecated. Please use `new` instead.
    Hi coala!
    >>> run(older='Hi')
    WARNING:root:The setting `older` is deprecated. Please use `new` instead.
    Hi!

    The metadata for coala has been adjusted as well:

    >>> list(run.__metadata__.non_optional_params.keys())
    ['new']
    >>> list(run.__metadata__.optional_params.keys())
    ['old', 'older']

    :param depr_args: A dictionary of settings as keys and their deprecated
                      names as values.
    """
    def _deprecate_decorator(func):

        logged_deprecated_args = set()

        def wrapping_function(*args, **kwargs):
            for arg, depr_value in wrapping_function.__metadata__.depr_values:
                deprecated_arg = depr_value[0]
                _func = depr_value[1]
                if deprecated_arg in kwargs:
                    if deprecated_arg not in logged_deprecated_args:
                        logging.warning(
                            'The setting `{}` is deprecated. Please use `{}` '
                            'instead.'.format(deprecated_arg, arg))
                        logged_deprecated_args.add(deprecated_arg)
                    depr_arg_value = _func.__call__(kwargs[deprecated_arg])
                    if arg in kwargs and depr_arg_value != kwargs[arg]:
                        logging.warning(
                            'The value of `{}` and `{}` are conflicting.'
                            ' `{}` will be used instead.'.format(
                                  deprecated_arg, arg, arg))
                    else:
                        kwargs[arg] = depr_arg_value
                    del kwargs[deprecated_arg]
            debug_bears = kwargs.get('debug_bears')
            if debug_bears:
                kwargs.pop('debug_bears')
                db.runcall(func,*args,**kwargs)


            return func(*args, **kwargs)

        new_metadata = FunctionMetadata.from_function(func)
        new_metadata.depr_values = []
        for arg, depr_values in depr_args.items():
            if not isinstance(depr_values, tuple):
                depr_values = (depr_values,)

            if callable(depr_values[-1]):
                deprecated_args = depr_values[:-1]
                default_modifier = depr_values[-1]
            else:
                deprecated_args = depr_values
                default_modifier = _do_nothing

            for depr_value in deprecated_args:
                if isinstance(depr_value, dict):
                    deprecated_arg = list(depr_value.keys())[0]
                    modifier = depr_value[deprecated_arg]
                    new_metadata.depr_values.append((arg,
                                                     (deprecated_arg,
                                                      modifier)))
                else:
                    deprecated_arg = depr_value
                    new_metadata.depr_values.append((arg,
                                                     (deprecated_arg,
                                                      default_modifier)))
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
