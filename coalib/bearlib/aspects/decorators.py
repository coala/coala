
from functools import wraps

from .taste import Taste
from .meta import aspectclass
from coalib.settings.FunctionMetadata import FunctionMetadata


def map_setting_to_aspect(**aspectable_setting):
    """
    Map function arguments with aspect and override it if appropriate.

    This decorator can be used by ``Bear.run()`` to automatically map and
    override bear's setting value with their equivalent aspect or taste.

    The order of setting override from the lowest to highest is:
    - Setting default (in bear's run argument)
    - aspect/taste default (if aspect is activated in Section)
    - Explicit aspect/taste default (if aspect is activated in Section)
    - Explicit setting

    :param aspectable_setting:
        A dictionary of settings as keys and their equivalent aspect or taste
        as value.
    """
    def _func_decorator(func):
        @wraps(func)
        def _new_func(self, *args, **kwargs):
            if self.section.aspects:
                aspects = self.section.aspects
                for arg, aspect_value in aspectable_setting.items():
                    # Explicit setting takes priority
                    if arg in self.section:
                        continue

                    if isinstance(aspect_value, aspectclass):
                        kwargs[arg] = aspects.get(aspect_value) is not None
                    if isinstance(aspect_value, Taste):
                        aspect_instance = aspects.get(aspect_value.aspect_name)
                        if aspect_instance:
                            kwargs[arg] = aspect_instance.tastes[
                                aspect_value.name]

            return func(self, *args, **kwargs)

        # Keep metadata
        _new_func.__metadata__ = FunctionMetadata.from_function(func)

        return _new_func

    return _func_decorator


def map_ambiguous_setting_to_aspect(**aspectable_settings):
    """
    Convert bear settings to use aspects in which there is some ambiguity.

    The ambiguity is because of differing values (maybe either name or even
    data-types) in bear settings and their corresponding aspect tastes.

    This decorator is used by ``Bear.run()`` to automatically map and
    override the value in the bear setting with their equivalent taste
    as provided in the parameter.

    The order of setting override from the highest to lowest is:
    - Explicit setting
    - Explicit aspect/taste default (if aspect is activated in Section)
    - aspect/taste default (if aspect is activated in Section)
    - Setting default (in bear's run argument)

    :param aspectable_settings:
        A dictionary in which keys are the bear settings and the corresponding
        value for each key is a tuple containing an equivalent taste as first
        value and a list of tuples with matching bear settings' and aspects'
        value as the second value.
    """
    def _func_decorator(func):
        @wraps(func)
        def _new_func(self, *args, **kwargs):
            if not self.section.aspects:
                return func(self, *args, **kwargs)

            aspects = self.section.aspects
            for arg, aspect_value in aspectable_settings.items():
                # Explicit bear setting takes priority over aspects
                if arg in self.section:
                    continue

                taste, aspect_settings = aspect_value
                aspect_instance = aspects.get(taste.aspect_name)
                if aspect_instance:
                    value = aspect_instance.tastes[taste.name]
                    for value_pair in aspect_value[1]:
                        if value_pair[0] == value:
                            kwargs[arg] = value_pair[1]

            return func(self, *args, **kwargs)

        # Keep metadata
        _new_func.__metadata__ = FunctionMetadata.from_function(func)

        return _new_func

    return _func_decorator
