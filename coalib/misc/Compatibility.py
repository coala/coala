try:
    # only available in Python > 3.4
    from importlib.util import module_from_spec
except ImportError:  # pragma Python 3.5,3.6: no cover
    from types import ModuleType

    def module_from_spec(spec):
        """
        Creates a new module object from given
        ``importlib.machinery.ModuleSpec`` instance.
        """
        module = ModuleType(spec.name)
        module.__file__ = spec.origin
        module.__loader__ = spec.loader
        return module


import json
try:
    JSONDecodeError = json.decoder.JSONDecodeError
except AttributeError:  # pragma Python 3.5,3.6: no cover
    JSONDecodeError = ValueError
