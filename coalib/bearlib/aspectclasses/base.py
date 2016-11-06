class aspectbase:
    """
    Base class for aspectclasses with common features for their instances.

    Derived classes must use
    :class:`coalib.bearlib.aspectclasses.meta.aspectclass` as metaclass.
    This is automatically handled by
    :meth:`coalib.bearlib.aspectclasses.meta.aspectclass.subaspect` decorator.
    """

    def __init__(self, **taste_values):
        """
        Instantiate an aspectclass with specific `taste_values`,
        including parent tastes.

        All values will be casted to the related taste cast types.

        Non-given tastes will get their default values.
        """
        for name, taste in type(self).tastes.items():
            value = taste.cast_type(
                taste_values.pop(name, taste.default))
            self.__dict__[name] = value

    @property
    def tastes(self):
        """
        Get a dictionary of all taste names mapped to their
        specific values, including parent tastes.
        """
        return {name: self.__dict__[name] for name in type(self).tastes}

    def __getattr__(self, name):
        """
        Get the specific values from parent aspect tastes.

        Own taste values are retrieved via descriptor
        :meth:`coalib.bearlib.aspectclasses.Taste.__get__`.
        """
        if name in type(self).tastes.items():
            return self.__dict__[name]

        raise AttributeError(
            "aspectclass instance %s has no attribute or taste "
            "named %s" % (repr(self), repr(name)))

    def __setattr__(self, name, value):
        """
        Don't allow taste value manipulations after instantiation
        of aspectclasses.
        """
        raise AttributeError(
            "can't set attributes of aspectclass instances")
