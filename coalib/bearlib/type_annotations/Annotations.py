import inspect
from functools import wraps

from coalib.settings.FunctionMetadata import FunctionMetadata
# The following ignore is added since the source code of some
# bears use type_list as type annotations to arguments.
# ignore PyUnusedCodeBear
from coalib.settings.Setting import typed_list


def add_value_checks(*settings):
    """
    Decorator for bears that checks a bear setting against a list
    of acceptable values.

    :param settings:
        A list of tuples containing bear setting as a string, and
        a list of acceptable values as the second value to the tuple.
    """
    def wrapping_function(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            args[0].ACCEPTABLE_VALUES_FOR_SETTINGS = settings[0]
            if hasattr(args[0], 'CALL_TO_POPULATE') and (
                    args[0].CALL_TO_POPULATE is True):
                return
            code = inspect.getsource(func)
            hoax_code = code[code.find('def'):code.find('):')+3].strip()
            hoax_code += '\n\treturn inspect.currentframe()\n'
            hoax_code = hoax_code.replace(func.__name__, 'hoax_method', 1)
            exec(hoax_code, globals(), globals())
            frame = hoax_method(*args, **kwargs)
            arguments, _, _, values = inspect.getargvalues(frame)
            for setting_name, acceptable_values in settings[0]:
                if values[setting_name] not in acceptable_values:
                    raise ValueError('Invalid value "%s" given to the bear'
                                     ' setting "%s"' % (values[setting_name],
                                                        setting_name))
        new_metadata = FunctionMetadata.from_function(func)
        wrapper.__metadata__ = new_metadata
        return wrapper
    return wrapping_function
