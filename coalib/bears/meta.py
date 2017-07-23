from collections import defaultdict

from coalib.bearlib.aspects.collections import AspectList
from coalib.bearlib.languages.Language import Languages


class bearclass(type):
    """
    Metaclass for :class:`coalib.bears.Bear.Bear` and therefore all bear
    classes.

    Pushing bears into the future... ;)
    """

    # by default a bear class has no aspects
    aspects = defaultdict(lambda: AspectList([]))

    def __new__(mcs, clsname, bases, clsattrs, *varargs, aspects=None,
                languages=None):
        return type.__new__(mcs, clsname, bases, clsattrs, *varargs)

    def __init__(cls, clsname, bases, clsattrs, *varargs, aspects=None,
                 languages=None):
        """
        Initializes the ``.aspects`` dict and ``.languages`` array on new
        bear classes from the mapping and the sequence given to the
        keyword-only `aspects` and `languages` arguments, respectively.
        """
        type.__init__(cls, clsname, bases, clsattrs, *varargs)
        if aspects is not None:
            cls.languages = Languages(languages)
            cls.aspects = defaultdict(
                lambda: AspectList([]),
                ((k, AspectList(v, languages=cls.languages))
                 for (k, v) in dict(aspects).items()))
