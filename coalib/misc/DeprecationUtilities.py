import logging


def check_deprecation(param_list):
    """
    Shows a deprecation warning message if the parameters
    passed are not ``None``.

    :param param_list:
        A dictionary of parameters with their names mapped
        to their values being checked for deprecation.

    >>> from testfixtures import LogCapture
    >>> from collections import OrderedDict
    >>> param_list = OrderedDict([('foo', None),
    ...                           ('bar', 'Random'),
    ...                           ('baz', 1773)])
    >>> with LogCapture() as capture:
    ...     check_deprecation(param_list)
    ...     print(capture)
    root WARNING
      bar parameter is deprecated
    root WARNING
      baz parameter is deprecated
    """
    for param_name, param_value in param_list.items():
        if param_value is not None:
            logging.warning('{} parameter is deprecated'.format(param_name))
