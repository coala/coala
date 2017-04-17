from collections import defaultdict

from coalib.bearlib.aspects.collections import aspectlist


class bearclass(type):
    """
    Metaclass for :class:`coalib.bears.Bear.Bear` and therefore all bear
    classes.

    Pushing bears into the future... ;)
    """

    # by default a bear class has no aspects
    aspects = defaultdict(lambda: aspectlist([]))

    def __new__(mcs, clsname, bases, clsattrs, *varargs, aspects=None):
        return type.__new__(mcs, clsname, bases, clsattrs, *varargs)

    def __init__(cls, clsname, bases, clsattrs, *varargs, aspects=None):
        """
        Initializes the ``.aspects`` dict on new bear classes from the mapping
        given to the keyword-only `aspects` argument.
        """
        type.__init__(cls, clsname, bases, clsattrs, *varargs)
        if aspects is not None:
            cls.aspects = defaultdict(
                lambda: aspectlist([]),
                ((k, aspectlist(v)) for (k, v) in dict(aspects).items()))
