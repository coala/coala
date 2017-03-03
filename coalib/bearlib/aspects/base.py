from coalib.bearlib.languages import Language

from .taste import TasteError


class aspectbase:
    """
    Base class for aspectclasses with common features for their instances.

    Derived classes must use
    :class:`coalib.bearlib.aspects.meta.aspectclass` as metaclass.
    This is automatically handled by
    :meth:`coalib.bearlib.aspects.meta.aspectclass.subaspect` decorator.
    """

    def __init__(self, language, **taste_values):
        """
        Instantiate an aspectclass with specific `taste_values`,
        including parent tastes.

        Given tastes must be available for the given `language`,
        which must be a language identifier supported by
        :class:`coalib.bearlib.languages.Language`.

        All taste values will be casted to the related taste cast types.

        Non-given available tastes will get their default values.
        """
        # bypass self.__setattr__
        self.__dict__['language'] = Language[language]
        for name, taste in type(self).tastes.items():
            if taste.languages and language not in taste.languages:
                if name in taste_values:
                    raise TasteError('%s.%s is not available for %s.' % (
                        type(self).__qualname__, name, language))
            else:
                setattr(self, name, taste_values.get(name, taste.default))

    def __eq__(self, other):
        return type(self) is type(other) and self.tastes == other.tastes

    @property
    def tastes(self):
        """
        Get a dictionary of all taste names mapped to their specific values,
        including parent tastes.
        """
        return {name: self.__dict__[name] for name in type(self).tastes
                if name in self.__dict__}

    def __setattr__(self, name, value):
        """
        Don't allow attribute manipulations after instantiation of
        aspectclasses.
        """
        if name not in type(self).tastes:
            raise AttributeError(
                "can't set attributes of aspectclass instances")
        super().__setattr__(name, value)
