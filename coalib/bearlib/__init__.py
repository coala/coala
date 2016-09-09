"""
The bearlib is an optional library designed to ease the task of any Bear. Just
as the rest of coala the bearlib is designed to be as easy to use as possible
while offering the best possible flexibility.
"""

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

     >>> run(old="Hello world!")
     The setting `old` is deprecated. Please use `new` instead.
     Hello world!
     >>> run(new="Hello world!")
     Hello world!

     This example represents the case where the old setting name needs to be
     modified to match the new one.

     >>> @deprecate_settings(new=('old', lambda a: a + 'coala!'))
     ... def func(new):
     ...     print(new)

     >>> func(old="Welcome to ")
     The setting `old` is deprecated. Please use `new` instead.
     Welcome to coala!
     >>> func(new='coala!')
     coala!

     This example represents the case where the old and new settings are
     provided to the function.

     >>> @deprecate_settings(new='old')
     ... def run(new):
     ...     print(new)
     >>> run(old="Hello!", new='coala is always written with lowercase `c`.')
     The setting `old` is deprecated. Please use `new` instead.
     The value of `old` and `new` are conflicting. `new` will be used instead.
     coala is always written with lowercase `c`.
     >>> run(old='Hello!', new='Hello!')
     The setting `old` is deprecated. Please use `new` instead.
     Hello!

     The metadata for coala has been adjusted as well:

     >>> list(run.__metadata__.non_optional_params.keys())
     ['new']
     >>> list(run.__metadata__.optional_params.keys())
     ['old']

     You cannot deprecate an already deprecated setting. Don't try. It will
     introduce nondeterministic errors to your program.

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
                    print("The setting `{}` is deprecated. Please use `{}` "
                          "instead.".format(deprecated_arg, arg))
                    depr_arg_value = _func.__call__(kwargs[deprecated_arg])
                    if arg in kwargs and depr_arg_value != kwargs[arg]:
                        print('The value of `{}` and `{}` are conflicting.'
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
            new_metadata.add_alias(arg, deprecated_arg)
        wrapping_function.__metadata__ = new_metadata

        return wrapping_function

    return _deprecate_decorator
