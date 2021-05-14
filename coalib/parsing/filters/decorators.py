from inspect import getmro
from functools import wraps


def typed_filter(type_classes, msg=None):
    """
    Used to enforce type of the first argument of a method
    by its class name as string. Raises NotImplementedError
    if the type does not match. Primarily used to enforce
    type of a filter.

    :param type_classes:    list or tuple of acceptable class names
                            as strings for the first argument of the
                            method being decorated.
    :param msg:             Message to pass with NotImplementedError.
    """
    if (type(type_classes) not in (tuple, list)):
        type_classes = (type_classes,)

    def decorator(filter):

        @wraps(filter)
        def decorated_filter(obj, *args, **kargs):
            obj_class = obj.__class__
            all_bases = list(map(lambda klass: klass.__name__,
                                 getmro(obj_class)))

            for type_class in type_classes:
                if str(type_class) in all_bases:
                    break
            else:
                raise NotImplementedError(
                    msg or f'\'{filter.__name__}\' can only handle'
                           f' {tuple(type_classes)}. '
                           'The context of your usage might be wrong.')

            return filter(obj, *args, **kargs)

        return decorated_filter

    return decorator
