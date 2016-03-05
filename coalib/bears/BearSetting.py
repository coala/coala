from coalib.misc.Decorators import (assert_right_type,
                                    enforce_signature,
                                    generate_eq)


# TODO Integrate that into `get_metadata` (/ call it `get_needed_settings`
# TODO or so)
@generate_eq("name", "type", "default")
class BearSetting:
    @enforce_signature
    def __init__(self, name: str, description: str, typ: type, default=None):
        assert_right_type(default, (None, typ), "default")

        self._name = name
        self._description = description
        self._type = typ
        self._default = default

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def type(self):
        return self._type

    @property
    def default(self):
        return self._default