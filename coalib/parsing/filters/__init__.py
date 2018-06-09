"""
This package holds filter functions. Filter objects are used to
get a list of bears with specific properties.
"""
from .LanguageFilter import language_filter
from .CanDetectFilter import can_detect_filter
from .CanFixFilter import can_fix_filter


available_filters = {'language': language_filter,
                     'can_detect': can_detect_filter,
                     'can_fix': can_fix_filter,
                     }
